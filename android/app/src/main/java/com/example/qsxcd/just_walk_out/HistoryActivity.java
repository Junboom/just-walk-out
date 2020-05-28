package com.example.qsxcd.just_walk_out;

import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;

import static com.example.qsxcd.just_walk_out.MainActivity.prefConfig;
import static com.example.qsxcd.just_walk_out.MainActivity.ROOT_URL;
import static com.example.qsxcd.just_walk_out.NavigationActivity.TAG_cardid;

public class HistoryActivity extends AppCompatActivity {

    private static final String TAG_station = "station";
    private static final String TAG_fair = "fair";
    private static final String TAG_state = "state";
    private static final String TAG_date ="date";
    private static final String TAG_time = "time";
    TextView rfcardid;
    LinearLayout empty;
    Retrofit retrofit;
    ApiService apiService;
    ArrayList<HashMap<String, String>> mArrayList;
    ListView mlistView;
    Button to, week, one, three, six, year;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //getSupportActionBar().setDisplayHomeAsUpEnabled(true); //뒤로가기

        try {
            getSupportActionBar().setDisplayOptions(ActionBar.DISPLAY_SHOW_CUSTOM);
            getSupportActionBar().setCustomView(R.layout.custom_bar);
            TextView custom_bar_text = (TextView) findViewById(R.id.custom_bar_text);
            custom_bar_text.setText("이용 기록");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        setContentView(R.layout.activity_history);

        rfcardid = (TextView) findViewById(R.id.rfcardid);
        rfcardid.setText(TAG_cardid);

        to=(Button) findViewById(R.id.to);
        week=(Button) findViewById(R.id.week);
        one=(Button) findViewById(R.id.one);
        three=(Button) findViewById(R.id.three);
        six=(Button) findViewById(R.id.six);
        year=(Button) findViewById(R.id.year);

        all();

        to.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                day_cal(1);
                prefConfig.displayToast("당일 기록");
            }
        });

        week.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                day_cal(8);
                prefConfig.displayToast("1주일 기록");
            }
        });

        one.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                day_cal(31);
                prefConfig.displayToast("1개월 기록");
            }
        });

        three.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                day_cal(92);
                prefConfig.displayToast("3개월 기록");
            }
        });

        six.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                day_cal(184);
                prefConfig.displayToast("6개월 기록");
            }
        });

        year.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                day_cal(366);
                prefConfig.displayToast("1년 기록");
            }
        });


    }

    public void all(){
        retrofit=new Retrofit.Builder().baseUrl(ROOT_URL).build();
        apiService=retrofit.create(ApiService.class);
        mlistView = (ListView) findViewById(R.id.listView);
        empty=(LinearLayout)findViewById(R.id.empty);
        mlistView.setEmptyView(empty);
        mArrayList = new ArrayList<>();
        //get
        Call<ResponseBody> comment = apiService.getPostrecord("1");
        comment.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
                try {
                    String result=response.body().string();
                    Log.v("Test", result);

                    try{
                        JSONArray jsonArray=new JSONArray(result); //json형식의 string을 객체에 저장

                        String id;
                        String station;
                        String cardid;
                        String fair;
                        String state;
                        String date;
                        String time;

                        //정수형: getInt(), 실수형: getDouble(), 문자: getString()
                        for(int i=0; i<jsonArray.length(); i++){
                            JSONObject jsonObject=jsonArray.getJSONObject(i);

                            id=jsonObject.getString("id");
                            station=jsonObject.getString("station");
                            cardid=jsonObject.getString("cardid");
                            fair=jsonObject.getString("fair");
                            state=jsonObject.getString("state");
                            date=jsonObject.getString("date");
                            time=jsonObject.getString("time");

                            Log.v("Test1", jsonObject.toString());
                            //Object 내용 확인: jsonObject.toString()
                            if(cardid.equals(TAG_cardid)){
                                HashMap<String,String> hashMap = new HashMap<>();

                                hashMap.put(TAG_station, station);
                                hashMap.put(TAG_fair, fair);
                                hashMap.put(TAG_state, state);
                                hashMap.put(TAG_date, date);
                                hashMap.put(TAG_time, time);

                                Log.v("Test2", hashMap.toString());

                                mArrayList.add(hashMap);
                            }

                        }
                        ListAdapter adapter = new SimpleAdapter(
                                HistoryActivity.this, mArrayList, R.layout.history_item,
                                new String[]{TAG_date, TAG_time, TAG_station, TAG_state, TAG_fair},
                                new int[]{R.id.textdate, R.id.texttime, R.id.textstation, R.id.textcase, R.id.textfare}
                        );

                        mlistView.setAdapter(adapter);
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
    }
    public void day_cal(final int day_num){
        final Calendar cal = Calendar.getInstance();
        int year = cal.get(Calendar.YEAR);
        int month = cal.get(Calendar.MONTH)+1;
        int day = cal.get(Calendar.DAY_OF_MONTH);
        final String today=year+"-"+month+"-"+day;

        Log.v("today", today);

        retrofit=new Retrofit.Builder().baseUrl(ROOT_URL).build();
        apiService=retrofit.create(ApiService.class);
        mlistView = (ListView) findViewById(R.id.listView);
        empty=(LinearLayout)findViewById(R.id.empty);
        mlistView.setEmptyView(empty);
        mArrayList = new ArrayList<>();
        //get
        Call<ResponseBody> comment = apiService.getPostrecord("1");
        comment.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
                try {
                    String result=response.body().string();
                    Log.v("Test", result);

                    try{
                        JSONArray jsonArray=new JSONArray(result); //json형식의 string을 객체에 저장

                        String id;
                        String station;
                        String cardid;
                        String fair;
                        String state;
                        String date;
                        String time;

                        //정수형: getInt(), 실수형: getDouble(), 문자: getString()
                        for(int i=0; i<jsonArray.length(); i++){
                            JSONObject jsonObject=jsonArray.getJSONObject(i);

                            id=jsonObject.getString("id");
                            station=jsonObject.getString("station");
                            cardid=jsonObject.getString("cardid");
                            fair=jsonObject.getString("fair");
                            state=jsonObject.getString("state");
                            date=jsonObject.getString("date");
                            time=jsonObject.getString("time");

                            Log.v("Test1", jsonObject.toString());
                            if(cardid.equals(TAG_cardid)){
                                if(doDiffOfDate(date,today) < day_num){
                                    HashMap<String,String> hashMap = new HashMap<>();

                                    hashMap.put(TAG_station, station);
                                    hashMap.put(TAG_fair, fair);
                                    hashMap.put(TAG_state, state);
                                    hashMap.put(TAG_date, date);
                                    hashMap.put(TAG_time, time);

                                    Log.v("Test2", hashMap.toString());

                                    mArrayList.add(hashMap);
                                }
                            }
                        }
                        ListAdapter adapter = new SimpleAdapter(
                                HistoryActivity.this, mArrayList, R.layout.history_item,
                                new String[]{TAG_date, TAG_time, TAG_station, TAG_state, TAG_fair},
                                new int[]{R.id.textdate, R.id.texttime, R.id.textstation, R.id.textcase, R.id.textfare}
                        );

                        mlistView.setAdapter(adapter);
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
    }

    public long doDiffOfDate(String start, String end) {
        long diffDays = 0;
        try {
            SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
            Date beginDate = formatter.parse(start);
            Date endDate = formatter.parse(end);

            // 시간차이를 시간,분,초를 곱한 값으로 나누면 하루 단위가 나옴
            long diff = endDate.getTime() - beginDate.getTime();
            diffDays = diff / (24 * 60 * 60 * 1000);

            System.out.println("날짜차이=" + diffDays);

        } catch (ParseException e) {
            e.printStackTrace();
        }

        return diffDays;
    }

}
