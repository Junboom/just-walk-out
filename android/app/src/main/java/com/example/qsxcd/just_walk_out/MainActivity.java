package com.example.qsxcd.just_walk_out;

import android.annotation.TargetApi;
import android.app.NotificationManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Handler;
import android.support.v4.app.NotificationCompat;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity{

    public static final String ROOT_URL = "http://54.85.63.115/";
    public static PrefConfig prefConfig;
    public static ApiService apiService;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        prefConfig=new PrefConfig(this);
        apiService=ApiClient.getApiClient().create(ApiService.class);

        try {
            getSupportActionBar().setDisplayOptions(ActionBar.DISPLAY_SHOW_CUSTOM);
            getSupportActionBar().setCustomView(R.layout.custom_bar);
            TextView custom_bar_text = (TextView) findViewById(R.id.custom_bar_text);
            custom_bar_text.setText("");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        setContentView(R.layout.activity_main);




        //alarm_message();
        startLoading();

    }

    private void startLoading(){
        Handler handler = new Handler();
        handler.postDelayed(new Runnable(){

            public void run(){
                if(prefConfig.readLoginStatus()){
                    Intent intent = new Intent(getBaseContext(), NavigationActivity.class);
                    startActivity(intent);
                    finish();
                }else{
                    Intent intent = new Intent(getBaseContext(), LoginActivity.class);
                    startActivity(intent);
                    finish();
                }
            }
        }, 2000);
    }

    private void alarm_message(){
        NotificationCompat.Builder mBuilder = new NotificationCompat.Builder(this);
        mBuilder.setSmallIcon(R.drawable.ic_home_black);
        mBuilder.setContentTitle("캡스톤디자인1(A) - 상상관203");
        mBuilder.setContentText("정상 출결 되었습니다");

        NotificationManager mNotificationManager =
                (NotificationManager)getSystemService(Context.NOTIFICATION_SERVICE);
// MY_NOTIFICATION_ID allows you to update the notification later on.
        mNotificationManager.notify(1, mBuilder.build());
    }



}
