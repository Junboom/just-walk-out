package com.example.qsxcd.just_walk_out;

import android.app.DatePickerDialog;
import android.app.NotificationManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.support.v4.app.NotificationCompat;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Html;
import android.util.Log;
import android.util.Patterns;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.RadioGroup;
import android.widget.Spinner;
import android.widget.TextView;

import java.util.Calendar;
import retrofit2.Call;

import static com.example.qsxcd.just_walk_out.MainActivity.ROOT_URL;
import static com.example.qsxcd.just_walk_out.MainActivity.apiService;
import static com.example.qsxcd.just_walk_out.MainActivity.prefConfig;

public class SignUpActivity extends AppCompatActivity {

    String insertdate;
    TextView text_birth;
    EditText edit_name, edit_email, edit_pw, edit_pwc, edit_phone, edit_rfid;
    Button btn_signup, btn_cancel;

    //public static final String ROOT_URL = "http://34.207.213.77/";

    private DatePickerDialog.OnDateSetListener mDateSetListener;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        /*
        try {
            getSupportActionBar().setDisplayOptions(ActionBar.DISPLAY_SHOW_CUSTOM);
            getSupportActionBar().setCustomView(R.layout.custom_bar);
            TextView custom_bar_text = (TextView) findViewById(R.id.custom_bar_text);
            custom_bar_text.setText("회원 가입");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }*/

        setContentView(R.layout.activity_sign_up);

        Intent intent = new Intent(getApplicationContext(), CameraActivity.class);
        startActivityForResult(intent, 1);


        edit_name = (EditText) findViewById(R.id.editText_name);
        edit_email = (EditText) findViewById(R.id.editText_email);
        edit_pw = (EditText) findViewById(R.id.editText_pw);
        edit_pwc = (EditText) findViewById(R.id.editText_pwc);
        text_birth = (TextView) findViewById(R.id.editText_date);
        edit_phone = (EditText) findViewById(R.id.editText_phone);
        edit_rfid = (EditText) findViewById(R.id.editText_rfid);
        btn_signup = (Button) findViewById(R.id.button_sign_up);
        btn_cancel = (Button) findViewById(R.id.button_cancel);

        //성별

        //생년월일
        text_birth.setText(Html.fromHtml("<u>생년월일 선택하기</u>"));
        text_birth.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v){
                Calendar cal = Calendar.getInstance();
                int year = cal.get(Calendar.YEAR);
                int month = cal.get(Calendar.MONTH);
                int day = cal.get(Calendar.DAY_OF_MONTH);

                DatePickerDialog dialog = new DatePickerDialog(
                        SignUpActivity.this, android.R.style.Theme_Holo_Light_Dialog_MinWidth, mDateSetListener, year, month, day);
                dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
                dialog.show();
            }
        });
        mDateSetListener = new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int year, int month, int day) {
                month = month + 1;
                //Log.d(TAG, "onDateSet: yyyy/mm/dd : " + year + "/" + month + "/" + day);

                String date = year + "년 " + month + "월 " + day + "일";
                insertdate = year + "-" + month + "-" + day + "";
                text_birth.setText(Html.fromHtml("<u>" + date + "</u>"));
            }
        };

        /*4번째 레트로핏*/
        btn_signup.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                performRegistration();
            }
        });

        btn_cancel.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                finish();
            }
        });
    }



    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        String a = data.getStringExtra("id");
        edit_rfid.setText(a);

    }






    public void performRegistration(){
        String name=edit_name.getText().toString();
        String email=edit_email.getText().toString();
        String password=edit_pw.getText().toString();
        String pwc=edit_pwc.getText().toString();
        String birth=text_birth.getText().toString();
        String phone=edit_phone.getText().toString();
        String rfid=edit_rfid.getText().toString();

        Log.e("name: ",name);
        Log.e("email: ",email);
        Log.e("password: ",password);
        Log.e("pwc: ",pwc);
        Log.e("birth: ",birth);
        Log.e("phone: ",phone);
        Log.e("rfid: ",rfid);

        if (validar()) {
            Log.e("validar: ", String.valueOf(validar()));

            Call<User> call=apiService.performRegistration(name, email, password, birth, phone, rfid);
            call.enqueue(new retrofit2.Callback<User>() {
                @Override
                public void onResponse(Call<User> call, retrofit2.Response<User> response) {
                    Log.e("response",response.body().getResponse());
                    if(response.body().getResponse().equals("ok")){
                        Log.e("register","Ok");
                        //LoginActivity.prefConfig.displayToast("Registration Success....");
                        prefConfig.displayToast("회원가입 완료");

                        alarm_message_sign();

                        edit_name.setText("");
                        edit_email.setText("");
                        edit_pw.setText("");
                        text_birth.setText(Html.fromHtml("<u>생년월일 선택하기</u>"));
                        edit_phone.setText("");
                        edit_rfid.setText("");

                        Intent intent = new Intent(getBaseContext(), LoginActivity.class);
                        startActivity(intent);

                    }else if(response.body().getResponse().equals("exist")){
                        Log.e("register","Exist");
                        //LoginActivity.prefConfig.displayToast("User already exist....");
                        prefConfig.displayToast("email 중복");

                    }else if(response.body().getResponse().equals("error")){
                        Log.e("register","Error");
                        //LoginActivity.prefConfig.displayToast("Something went wrong....");
                        prefConfig.displayToast("회원가입 오류");
                    }
                }

                @Override
                public void onFailure(Call<User> call, Throwable t) {
                    Log.e("register","onFailure");
                }
            });
        }else{
            Log.e("validar: ", String.valueOf(validar()));
        }

        //Call<User> call=MainActivity.apiInterface.performRegistration(name, email, password);
        /*
        Call<User> call=FirstActivity.apiInterface.performRegistration(name, email, password, birth, phone, rfid);

        call.enqueue(new retrofit2.Callback<User>() {
            @Override
            public void onResponse(Call<User> call, retrofit2.Response<User> response) {
                Log.e("response",response.body().getResponse());
                if(response.body().getResponse().equals("ok")){
                    Log.e("register","Ok");
                    //FirstActivity.prefConfig.displayToast("Registration Success....");
                    FirstActivity.prefConfig.displayToast("회원가입 완료");

                    edit_name.setText("");
                    edit_email.setText("");
                    edit_pw.setText("");
                    text_birth.setText(Html.fromHtml("<u>생년월일 선택하기</u>"));
                    edit_phone.setText("");
                    edit_rfid.setText("");

                    Intent intent = new Intent(getBaseContext(), FirstActivity.class);
                    startActivity(intent);

                }else if(response.body().getResponse().equals("exist")){
                    Log.e("register","Exist");
                    //FirstActivity.prefConfig.displayToast("User already exist....");
                    FirstActivity.prefConfig.displayToast("email 중복");

                }else if(response.body().getResponse().equals("error")){
                    Log.e("register","Error");
                    //FirstActivity.prefConfig.displayToast("Something went wrong....");
                    FirstActivity.prefConfig.displayToast("회원가입 오류");
                }
            }

            @Override
            public void onFailure(Call<User> call, Throwable t) {
                Log.e("register","onFailure");
            }
        });
        */
    }

    private boolean validar() {
        boolean valid = true;

        String name=edit_name.getText().toString();
        String email=edit_email.getText().toString();
        String password=edit_pw.getText().toString();
        String pwc=edit_pwc.getText().toString();
        String birth=text_birth.getText().toString();
        String phone=edit_phone.getText().toString();
        String rfid=edit_rfid.getText().toString();

        if (email.isEmpty() || !android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            edit_email.setError("유효한 email 형식을 입력해주세요.");
            valid = false;
        } else {
            edit_email.setError(null);
        }
        if (password.isEmpty() || password.length() < 6 || password.length() > 10) {
            edit_pw.setError("6~10자리의 비밀번호를 입력해주세요.");
            valid = false;
        }else{
            edit_pw.setError(null);
        }
        if (!pwc.equals(password)) {
            edit_pwc.setError("비밀번호가 일치하지 않습니다.");
            valid = false;
        }else{
            edit_pwc.setError(null);
        }
        if (birth.isEmpty()) {
            prefConfig.displayToast("생년월일을 선택해주세요.");
            valid = false;
        }else{
            text_birth.setError(null);
        }
        if (phone.isEmpty() || !Patterns.PHONE.matcher(phone).matches()) {
            edit_phone.setError("유효한 휴대폰을 입력해주세요.");
            valid = false;
        }else{
            edit_phone.setError(null);
        }
        return valid;
    }

    private void alarm_message_sign(){
        NotificationCompat.Builder mBuilder = new NotificationCompat.Builder(this);
        mBuilder.setSmallIcon(R.drawable.logo);
        mBuilder.setContentTitle("Just WALK OUT");
        mBuilder.setContentText("회원가입이 완료되었습니다.");

        NotificationManager mNotificationManager =
                (NotificationManager)getSystemService(Context.NOTIFICATION_SERVICE);
// MY_NOTIFICATION_ID allows you to update the notification later on.
        mNotificationManager.notify(1, mBuilder.build());
    }
}
