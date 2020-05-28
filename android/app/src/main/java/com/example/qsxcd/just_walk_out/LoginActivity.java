package com.example.qsxcd.just_walk_out;

import android.annotation.SuppressLint;
import android.annotation.TargetApi;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.util.Patterns;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import static com.example.qsxcd.just_walk_out.MainActivity.apiService;
import static com.example.qsxcd.just_walk_out.MainActivity.prefConfig;

public class LoginActivity extends AppCompatActivity {

    private EditText Email, Password;
    private Button LoginBn, RegBn;
    private final int  MY_PERMISSION_REQUEST_STORAGE = 100;
    CheckBox checkbox_auto_login, checkbox_remember_email;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        //checkPermission(Contact.PERMISSIONS);

        RegBn=findViewById(R.id.button_sign_up);

        Email=findViewById(R.id.IDInput);
        Password=findViewById(R.id.PWInput);
        LoginBn=findViewById(R.id.button_login);
        checkbox_auto_login=findViewById(R.id.checkbox_auto_login);
        checkbox_remember_email=findViewById(R.id.checkbox_remember_email);

        if(prefConfig.readNum().equals("0")){
            checkbox_auto_login.setChecked(true);
        }else if(prefConfig.readNum().equals("1")){
            checkbox_auto_login.setChecked(false);
        }

        if(prefConfig.readNumId().equals("0")){//아이디 저장 시
            checkbox_remember_email.setChecked(true);
            Email.setText(prefConfig.readName());
        }else if(prefConfig.readNumId().equals("1")){
            checkbox_remember_email.setChecked(false);
        }

        LoginBn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                performLogin();
            }
        });

        RegBn.setOnClickListener(new View.OnClickListener(){

            @Override
            public void onClick(View view) {

                Intent intent = new Intent(LoginActivity.this, SignUpActivity.class);
                startActivity(intent);
            }
        });
    }





    private void performLogin(){
        final String email=Email.getText().toString();
        String password=Password.getText().toString();

        if (validar()) {
            Log.e("validar: ", String.valueOf(validar()));
            Log.e("email: ",email);
            Log.e("password: ",password);

            Call<User> call=apiService.performUserLogin(email, password);
            call.enqueue(new Callback<User>() {
                @Override
                public void onResponse(Call<User> call, Response<User> response) {

                    Log.e("response: ",response.body().getResponse());

                    if(response.body().getResponse().equals("ok")){
                        Log.e("login","Ok");
//                    Log.e("login_Name",response.body().getName());
                        prefConfig.displayToast("Login Success...");
                        Intent intent =new Intent(getApplicationContext(),NavigationActivity.class);
                        Log.e("checked", String.valueOf(checkbox_auto_login.isChecked()));
                        if(checkbox_auto_login.isChecked()){//자동로그인
                            prefConfig.writeLoginStatus(true);
                            prefConfig.writeName(email);
                            prefConfig.writeNum("0");
                        }else{
                            prefConfig.writeNum("1");
                            intent.putExtra("email", email);
                        }

                        if(checkbox_remember_email.isChecked()){//아이디 저장
                            prefConfig.writeName(email);
                            prefConfig.writeNumId("0");
                        }else{
                            prefConfig.writeNumId("1");
                        }

                        startActivity(intent);
                        finish();
                        Email.setText("");
                        Password.setText("");
                    }else if(response.body().getResponse().equals("failed")){
                        Log.e("login","Failed");
                        prefConfig.displayToast("Login Failed.. Please try again...");
                        Password.setText("");
                    }
                }
                @Override
                public void onFailure(Call<User> call, Throwable t) {
                    Log.e("login","onFailure");
                }
            });

        }else{
            Log.e("validar: ", String.valueOf(validar()));
        }
    }

    private boolean validar() {
        boolean valid = true;

        String email=Email.getText().toString();
        String password=Password.getText().toString();

        if (email.isEmpty() || !android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            Email.setError("유효한 email 형식을 입력해주세요.");
            //LoginActivity.prefConfig.displayToast("유효한 email 형식을 입력해주세요.");
            valid = false;
        } else {
            Email.setError(null);
        }
        if (password.isEmpty() || password.length() < 6 || password.length() > 10) {
            Password.setError("6~10자리의 비밀번호를 입력해주세요.");
            //LoginActivity.prefConfig.displayToast("6~10자리의 비밀번호를 입력해주세요.");
            valid = false;
        }else{
            Password.setError(null);
        }
        return valid;
    }





/*
    // 권한체크
    private void checkPermission(String[] permissions){
        requestPermissions(permissions, MY_PERMISSION_REQUEST_STORAGE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        switch (requestCode) {
            case MY_PERMISSION_REQUEST_STORAGE:
                int cnt = permissions.length;
                for (int i = 0; i < cnt; i++) {

                    if (grantResults[i] == PackageManager.PERMISSION_GRANTED) {

                        //Log.i(LOG_TAG, "Permission[" + permissions[i] + "] = PERMISSION_GRANTED");

                    } else {

                    }
                }
                break;
        }
    }*/
}
