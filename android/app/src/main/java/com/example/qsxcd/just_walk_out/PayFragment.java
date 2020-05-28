package com.example.qsxcd.just_walk_out;


import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TabHost;
import android.widget.TextView;


/**
 * A simple {@link Fragment} subclass.
 */


import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;

import static com.example.qsxcd.just_walk_out.MainActivity.ROOT_URL;
import static com.example.qsxcd.just_walk_out.NavigationActivity.TAG_phone;
import static com.example.qsxcd.just_walk_out.NavigationActivity.TAG_cardid;

public class PayFragment extends Fragment {

    static String TAG_bank_name, TAG_account_num, TAG_acc_holder, TAG_regist_num;

    Retrofit retrofit;
    ApiService apiService;

    TextView button_bank_change, custom_bank, custom_bank_num, custom_name, custom_phone, custom_rfid;
    TabHost tabHost;

    public PayFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        View view=inflater.inflate(R.layout.fragment_pay, container, false);

        custom_bank=(TextView) view.findViewById(R.id.custom_bank);
        custom_bank_num=(TextView) view.findViewById(R.id.custom_bank_num);
        custom_name=(TextView) view.findViewById(R.id.custom_name);
        custom_phone=(TextView) view.findViewById(R.id.custom_phone);
        custom_rfid=(TextView) view.findViewById(R.id.custom_rfid);

        getBankInfo();

        custom_phone.setText(TAG_phone);
        custom_rfid.setText(TAG_cardid);

        button_bank_change=(TextView)view.findViewById(R.id.button_bank_change);
        button_bank_change.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){

                FragmentManager fragmentManager = getFragmentManager();
                fragmentManager.beginTransaction().replace(R.id.NavFrag, new PayWayFragment()).commit();

                /*
                Fragment fragment = new PayWayFragment();
                FragmentManager fragmentManager = getFragmentManager();
                FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
                fragmentTransaction.replace(R.id.NavFrag, fragment);
                fragmentTransaction.commit();
                */
            }
        });

        tabHost=(TabHost)view.findViewById(R.id.TabHost);

        tabHost.setup();
        tabHost.addTab(tabHost.newTabSpec("A").setContent(R.id.tab1).setIndicator("청구내역"));
        tabHost.addTab(tabHost.newTabSpec("B").setContent(R.id.tab2).setIndicator("납부관리"));

        return view;
    }

    public void getBankInfo(){
        retrofit=new Retrofit.Builder().baseUrl(ROOT_URL).build();
        apiService=retrofit.create(ApiService.class);
        Call<ResponseBody> comment = apiService.getPostBank(TAG_cardid);
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
                            TAG_bank_name=jsonObject.getString("bank_name");
                            TAG_account_num=jsonObject.getString("account_num");
                            TAG_acc_holder=jsonObject.getString("acc_holder");
                            TAG_regist_num=jsonObject.getString("regist_num");

                            Log.v("payway", jsonObject.toString()); //Object 내용 확인: jsonObject.toString()
                            custom_bank.setText(TAG_bank_name);
                            custom_bank_num.setText(TAG_account_num);
                            custom_name.setText(TAG_acc_holder);
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
    }

}
