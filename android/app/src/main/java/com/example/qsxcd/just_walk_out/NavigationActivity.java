package com.example.qsxcd.just_walk_out;

import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.util.Log;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ListAdapter;
import android.widget.SimpleAdapter;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;

import static com.example.qsxcd.just_walk_out.MainActivity.ROOT_URL;
import static com.example.qsxcd.just_walk_out.MainActivity.prefConfig;

public class NavigationActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener{

    /*
    private static final String TAG_name = "name";
    private static final String TAG_email ="email";
    private static final String TAG_password = "password";
    private static final String TAG_birth = "birth";
    private static final String TAG_phone ="phone";
    private static final String TAG_cardid = "rfid";
    */
    static String TAG_name;
    static String TAG_email;
    static String TAG_password;
    static String TAG_birth;
    static String TAG_phone;
    static String TAG_cardid;
    Retrofit retrofit;
    ApiService apiService;
    ArrayList<HashMap<String, String>> mArrayList;

    private BackPressCloseHandler backPressCloseHandler;

    //private User user;
    /*
    final String UserName;
    final String UserEmail;
    final String UserPw;
    final String UserBirth;
    final String UserPhone;
    final String UserRf;

    public NavigationActivity(String userName, String userEmail, String userPw, String userBirth, String userPhone, String userRf) {
        UserName = userName;
        UserEmail = userEmail;
        UserPw = userPw;
        UserBirth = userBirth;
        UserPhone = userPhone;
        UserRf = userRf;
    }
*/
    OnLogoutListener logoutListener;

    public interface OnLogoutListener{
        public void logoutPerformed();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_navigation);

        backPressCloseHandler = new BackPressCloseHandler(this);

        String UserEmail = "";

        Intent intent=getIntent();
        Log.e("num",prefConfig.readNum());
        if(prefConfig.readNum().equals("0")){
            Log.e("0","자동로그인");
            UserEmail= prefConfig.readName();
        }else if(prefConfig.readNum().equals("1")){
            Log.e("1","일반로그인");
            UserEmail=intent.getStringExtra("email");
        }

//        Log.e("Navi_Email",UserEmail);
        //final String UserName=intent.getStringExtra("name");
        //Log.e("Navi_Name",UserName);

        retrofit=new Retrofit.Builder().baseUrl(ROOT_URL).build();
        apiService=retrofit.create(ApiService.class);
        Call<ResponseBody> comment = apiService.getPostuser(UserEmail);
        comment.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
                try {
                    String result=response.body().string();
                    Log.v("Test", result);

                    try{
                        JSONArray jsonArray=new JSONArray(result); //json형식의 string을 객체에 저장

                        //정수형: getInt(), 실수형: getDouble(), 문자: getString()
                        for(int i=0; i<jsonArray.length(); i++){
                            JSONObject jsonObject=jsonArray.getJSONObject(i);
/*
                            final String UserName=jsonObject.getString("name");
                            final String UserEmail=jsonObject.getString("email");
                            final String UserPw=jsonObject.getString("password");
                            final String UserBirth=jsonObject.getString("birth");
                            final String UserPhone=jsonObject.getString("phone");
                            final String UserRf=jsonObject.getString("rfid");
*/
                            TAG_name=jsonObject.getString("name");
                            TAG_email=jsonObject.getString("email");
                            TAG_password=jsonObject.getString("password");
                            TAG_birth=jsonObject.getString("birth");
                            TAG_phone=jsonObject.getString("phone");
                            TAG_cardid=jsonObject.getString("rfid");
                            if(TAG_email.equals("AA12SS34")){}
                            Log.v("Navi", jsonObject.toString());
                            //Object 내용 확인: jsonObject.toString()
                            View header = ((NavigationView)findViewById(R.id.nav_view)).getHeaderView(0);
                            ((TextView) header.findViewById(R.id.Name)).setText(TAG_name);
                            ((TextView) header.findViewById(R.id.Email)).setText(TAG_email);
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {

            }
        });

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        //default fragment

        android.support.v4.app.FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        ft.replace(R.id.NavFrag, new HomeFragment());
        ft.commit();

        navigationView.setCheckedItem(R.id.nav_home);
    }

    //액션바 이름
    public void setActionBarTitle(String title){
        getSupportActionBar().setTitle(title);
    }
/*
    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }

        long tempTime = System.currentTimeMillis();
        long intervalTime = tempTime - backPressedTime;

        if (0 <= intervalTime && FINISH_INTERVAL_TIME >= intervalTime){
            super.onBackPressed();
        }
        else{
            backPressedTime = tempTime;
            Toast.makeText(getApplicationContext(), "한번 더 뒤로가기를 누르면 앱이 종료됩니다.", Toast.LENGTH_SHORT).show();
        }
    }
*/
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.navigation, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
/*
        if (id == R.id.action_settings) {
            return true;
        }
*/
        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_home) {
            // Handle the camera action
            android.support.v4.app.FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
            ft.replace(R.id.NavFrag, new HomeFragment());
            ft.addToBackStack(null);
            ft.commit();
        } else if (id == R.id.nav_viewPay) {
            android.support.v4.app.FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
            ft.replace(R.id.NavFrag, new ViewPayFragment());
            ft.commit();
        } else if (id == R.id.nav_myPage) {
            android.support.v4.app.FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
            ft.replace(R.id.NavFrag, new MyPageFragment());
            ft.commit();
        } else if (id == R.id.nav_customerSupport) {
            android.support.v4.app.FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
            ft.replace(R.id.NavFrag, new CustomerSupportFragment());
            ft.commit();
        } else if (id == R.id.nav_setting) {
            android.support.v4.app.FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
            ft.replace(R.id.NavFrag, new SettingFragment());
            ft.commit();
        } else if (id == R.id.nav_logOut) {


            new AlertDialog.Builder(this, 0)
                    .setTitle("로그아웃").setMessage("로그아웃 하시겠습니까?")
                    .setPositiveButton("로그아웃", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int whichButton) {
                            prefConfig.writeLoginStatus(false);
                            //prefConfig.writeName("User");
                            prefConfig.writeNum("1");
                            Intent i = new Intent(NavigationActivity.this, LoginActivity.class);
                            i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP|Intent.FLAG_ACTIVITY_SINGLE_TOP);
                            startActivity(i);

                        }
                    })
                    .setNegativeButton("취소", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int whichButton) {

                        }
                    }).show();
        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }
/*
    public void logoutPerformed() {
        prefConfig.writeLoginStatus(false);
        prefConfig.writeName(TAG_name);
        Intent intent = new Intent(NavigationActivity.this, LoginActivity.class);
        startActivity(intent);
        /*
        getSupportFragmentManager()
                .beginTransaction()
                .replace(R.id.fragment_container, new LoginFragment())
                .addToBackStack(null)
                .commit();
                //
    }*/

    @Override public void onBackPressed(){
        //super.onBackPressed();
        backPressCloseHandler.onBackPressed();
    }
}
