package com.example.qsxcd.just_walk_out;

/**
 * Created by qsxcd on 2018-05-23.
 */

import android.app.Activity;
import android.widget.Toast;
public class BackPressCloseHandler{
    private long backKeyPressedTime=0;
    private Toast toast;
    private Activity activity;

    public BackPressCloseHandler(Activity context){
        this.activity=context;
    }

    public void onBackPressed(){
        if(System.currentTimeMillis()>backKeyPressedTime+2000){
            backKeyPressedTime=System.currentTimeMillis();
            showToast();
            return;
        }

        if(System.currentTimeMillis()<=backKeyPressedTime+2000) {
            activity.finish();
            toast.cancel();
        }
    }

    public void showToast(){
        toast=Toast.makeText(activity,"\'뒤로\'버튼을 한번 더 누르시면 종료됩니다.", Toast.LENGTH_SHORT);
        toast.show();
    }
}
