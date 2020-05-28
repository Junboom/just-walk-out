package com.example.qsxcd.just_walk_out;

/**
 * Created by qsxcd on 2018-05-13.
 */
import android.content.Context;
import android.content.SharedPreferences;
import android.widget.Toast;

public class PrefConfig {
    private SharedPreferences sharedPreferences;
    private Context context;

    public PrefConfig(Context context){
        this.context=context;
        sharedPreferences=context.getSharedPreferences(context.getString(R.string.pref_file), Context.MODE_PRIVATE);

    }
    public void writeLoginStatus(boolean status){
        SharedPreferences.Editor editor=sharedPreferences.edit();
        editor.putBoolean(context.getString(R.string.pref_login_status),status);
        editor.commit();
    }

    public boolean readLoginStatus(){
        return sharedPreferences.getBoolean(context.getString(R.string.pref_login_status),false);
    }

    public void writeName(String name){
        SharedPreferences.Editor editor=sharedPreferences.edit();
        editor.putString(context.getString(R.string.pref_user_name),name);
        editor.commit();
    }

    public String readName(){
        return sharedPreferences.getString(context.getString(R.string.pref_user_name),"User");
    }

    public void writeNum(String num){
        SharedPreferences.Editor editor=sharedPreferences.edit();
        editor.putString(context.getString(R.string.pref_num_auto),num);
        editor.commit();
    }

    public String readNum(){
        return sharedPreferences.getString(context.getString(R.string.pref_num_auto),"1");
    }

    public void writeNumId(String num){
        SharedPreferences.Editor editor=sharedPreferences.edit();
        editor.putString(context.getString(R.string.pref_num_id),num);
        editor.commit();
    }

    public String readNumId(){
        return sharedPreferences.getString(context.getString(R.string.pref_num_id),"1");
    }

    public void displayToast(String message){
        Toast.makeText(context, message, Toast.LENGTH_SHORT).show();
    }
}