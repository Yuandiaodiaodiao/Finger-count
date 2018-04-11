package com.yuan.finger;

import android.Manifest;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.provider.Settings;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

import okhttp3.Call;

public class MainActivity extends AppCompatActivity {
    private static int REQUEST_CAMERA = 1;

    private String[] permissions = {
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.INTERNET,
            Manifest.permission_group.STORAGE,
            Manifest.permission.CAMERA
    };
    private AlertDialog dialog;




    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 123) {

            if (android.os.Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                // 检查该权限是否已经获取
                int i = ContextCompat.checkSelfPermission(this, permissions[0]);
                int i1 = ContextCompat.checkSelfPermission(this, permissions[3]);
                // 权限是否已经 授权 GRANTED---授权  DINIED---拒绝
                if (i != PackageManager.PERMISSION_GRANTED||i1!=PackageManager.PERMISSION_GRANTED) {
                    // 提示用户应该去应用设置界面手动开启权限
                    showDialogTipUserGoToAppSettting();
                } else {
                    if (dialog != null && dialog.isShowing()) {
                        dialog.dismiss();
                    }
                    Toast.makeText(this, "权限获取成功", Toast.LENGTH_SHORT).show();
                }
            }
        }


        if (REQUEST_CAMERA == requestCode||requestCode==233) {
            postimage();
        }

    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {

            // 检查该权限是否已经获取
            int i = ContextCompat.checkSelfPermission(this, permissions[0]);
            // 权限是否已经 授权 GRANTED---授权  DINIED---拒绝
            if (i != PackageManager.PERMISSION_GRANTED) {
                // 如果没有授予该权限，就去提示用户请求
                showDialogTipUserRequestPermission();
            }
        }


        android.support.design.widget.FloatingActionButton bt = (android.support.design.widget.FloatingActionButton) findViewById(R.id.button1);
        if(Build.VERSION.SDK_INT < Build.VERSION_CODES.M){
            Toast.makeText(MainActivity.this,"小于apiN" , Toast.LENGTH_SHORT).show();
        bt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent opencamera = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                Uri imageUri = Uri.fromFile(new File(Environment.getExternalStorageDirectory(), "233.jpg"));
                opencamera.putExtra(MediaStore.EXTRA_OUTPUT, imageUri);

                startActivityForResult(opencamera, REQUEST_CAMERA);

            }
        });}
        else
            {
            bt.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    File file = new File(Environment.getExternalStorageDirectory(), "233.jpg");
                    Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N){
                        intent.putExtra(MediaStore.EXTRA_OUTPUT,
                                FileProvider.getUriForFile(MainActivity.this,"com.yuan.finger.fileprovider", file));
                    }else {
                        intent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(file));
                    }
                    startActivityForResult(intent, 233);


                }
            });

        }

    }


    public class MyStringCallback extends StringCallback {


        @Override
        public void onError(Call call, Exception e, int id) {
            Toast.makeText(MainActivity.this, "erros" + e.toString() + call.toString(), Toast.LENGTH_LONG).show();
        }

        @Override
        public void onResponse(String response, int id) {
            ProgressBar ps = (ProgressBar) findViewById(R.id.progressBar);
            ps.setVisibility(View.INVISIBLE);
            TextView tv = (TextView) findViewById(R.id.textView1);
            tv.setText("手指根数为" + response + "根");
            Toast.makeText(MainActivity.this, response, Toast.LENGTH_LONG).show();
        }
    }

private void postimage(){

    TextView tx = (TextView) findViewById(R.id.textView1);
    tx.setText("正在分析...");
    ProgressBar ps = (ProgressBar) findViewById(R.id.progressBar);
    ps.setVisibility(View.VISIBLE);
    File file = new File(Environment.getExternalStorageDirectory(), "233.jpg");
    if (!file.exists()) {
        Toast.makeText(MainActivity.this, "文件不存在，请修改文件路径", Toast.LENGTH_SHORT).show();
        return;
    }



    InputStream in = null;
    byte[] datasz = null;
    //读取图片字节数组
    ImageView im = (ImageView) findViewById(R.id.imageView1);

    Bitmap bm = null;
    try {
        bm = BitmapFactory.decodeStream(new FileInputStream(file));

    } catch (FileNotFoundException e) {
        e.printStackTrace();
    }
//            if(readPictureDegree(Environment.getExternalStorageDirectory()+"233.jpg")==90){
//                bm=toturn(bm);
//            }
//            Toast.makeText(MainActivity.this,"角度"+readPictureDegree(Environment.getExternalStorageDirectory()+"233.jpg")+"" , Toast.LENGTH_SHORT).show();
    while (bm.getWidth() > 4095 || bm.getHeight() > 4095) {
        Matrix matrix = new Matrix();
        matrix.setScale(0.5f, 0.5f);
        bm = Bitmap.createBitmap(bm, 0, 0, bm.getWidth(),
                bm.getHeight(), matrix, true);
    }
    im.setImageBitmap(bm);


//            while (bm.getWidth() > 1600 || bm.getHeight() > 1600) {
//                Matrix matrix = new Matrix();
//                matrix.setScale(0.5f, 0.5f);
//                bm = Bitmap.createBitmap(bm, 0, 0, bm.getWidth(),
//                        bm.getHeight(), matrix, true);
//            }
//
//            File avaterFile = new File(Environment.getExternalStorageDirectory(), "233.jpg");//设置文件名称
//            if(avaterFile.exists()){
//                avaterFile.delete();
//            }
//            try {
//                avaterFile.createNewFile();
//                FileOutputStream fos = new FileOutputStream(avaterFile);
//                bm.compress(Bitmap.CompressFormat.JPEG, 100, fos);
//                fos.flush();
//                fos.close();
//            } catch (IOException e) {
//                e.printStackTrace();
//            }
//            Toast.makeText(MainActivity.this, "照片已储存至:" + Environment.getExternalStorageDirectory() + "233.jpg", Toast.LENGTH_SHORT).show();
    try {
        try {
            in = new FileInputStream(file);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        datasz = new byte[in.available()];
        in.read(datasz);
        in.close();
    } catch (IOException e) {
        e.printStackTrace();
    }
    String sx = "";
    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
        sx = Base64.getEncoder().encodeToString(datasz);
//                       Toast.makeText(MainActivity.this, "编码", Toast.LENGTH_SHORT).show();
    }
//                   Toast.makeText(MainActivity.this, datasz.toString(), Toast.LENGTH_SHORT).show();
    sx = android.util.Base64.encodeToString(datasz, android.util.Base64.NO_WRAP);

    Map<String, String> map1 = new HashMap<String, String>();
    map1.put("233", sx);
    JSONArray jsons = new JSONArray();
    jsons.put(map1);
    JSONObject job = new JSONObject();
    try {
        job.put("jas", sx);
    } catch (JSONException e) {
        e.printStackTrace();
    }
    EditText te=(EditText)findViewById(R.id.editText);
    String urll=te.getText().toString();
//            if(urll.equals("http://oops-sdu.org:1025/finger")||urll.equals("http://101.76.241.9:1025/finger")) {
//                   Toast.makeText(MainActivity.this, job.toString(), Toast.LENGTH_SHORT).show();
    Log.d("233333333333", "23333");
    OkHttpUtils.postString()
//                           .url("http://oops-sdu.org:1025/finger")
            .url(urll)
            .content(job.toString())
            .build()

            .execute(new MyStringCallback());
//            }
//            else{
//        Toast.makeText(MainActivity.this, "无效的服务器地址", Toast.LENGTH_SHORT).show();}






}

    /*

    下面的是在android6 以上获取文件权限的代码
    *****************************************
    ******************************************


     */

    private void showDialogTipUserRequestPermission() {
//USED
        new AlertDialog.Builder(this)
                .setTitle("存储权限不可用")
                .setMessage("需要打开权限")
                .setPositiveButton("立即开启", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        startRequestPermission();
                    }
                })
                .setNegativeButton("取消", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        finish();
                    }
                }).setCancelable(false).show();
    }

    private void startRequestPermission() {
        //used
        if(Build.VERSION.SDK_INT < Build.VERSION_CODES.N) {
            ActivityCompat.requestPermissions(this, permissions, 321);
        }else{
             String[] permissions2 = {
                    Manifest.permission.WRITE_EXTERNAL_STORAGE,
                    Manifest.permission.INTERNET,
                    Manifest.permission_group.STORAGE,
                     Manifest.permission.CAMERA
            };
            ActivityCompat.requestPermissions(this, permissions2, 321);
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        if (requestCode == 321) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                if (grantResults[0] != PackageManager.PERMISSION_GRANTED) {
                    // 判断用户是否 点击了不再提醒。(检测该权限是否还可以申请)
                    boolean b = shouldShowRequestPermissionRationale(permissions[0]);
                    if (!b) {
                        // 用户还是想用我的 APP 的
                        // 提示用户去应用设置界面手动开启权限
                        showDialogTipUserGoToAppSettting();
                    } else
                        finish();
                } else {
                    Toast.makeText(this, "权限获取成功", Toast.LENGTH_SHORT).show();
                }
            }
        }
    }


    private void showDialogTipUserGoToAppSettting() {
//used
        dialog = new AlertDialog.Builder(this)
                .setTitle("存储权限不可用")
                .setMessage("请在-应用设置-权限-中，开启储存权限")
                .setPositiveButton("立即开启", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        // 跳转到应用设置界面
                        goToAppSetting();
                    }
                })
                .setNegativeButton("取消", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        finish();
                    }
                }).setCancelable(false).show();
    }

    // 跳转到当前应用的设置界面
    private void goToAppSetting() {
        //used
        Intent intent = new Intent();
        intent.setAction(Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
        Uri uri = Uri.fromParts("package", getPackageName(), null);
        intent.setData(uri);
        startActivityForResult(intent, 123);
    }


}
