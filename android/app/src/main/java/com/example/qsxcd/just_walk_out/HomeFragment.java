package com.example.qsxcd.just_walk_out;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;
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
import static com.example.qsxcd.just_walk_out.NavigationActivity.TAG_cardid;

public class HomeFragment extends Fragment {
    TextView textView14, textView10, textView15;
    public int TAG_total_fair;

    Retrofit retrofit;
    ApiService apiService;

    public HomeFragment() {
        // Required empty public constructor
    }

/*
@Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        ((NavigationActivity)getActivity()).setActionBarTitle("홈"); //액션바 이름

        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_home, container, false);
    }

*/
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view=inflater.inflate(R.layout.fragment_home, container, false);

//        UserName = LoginActivity.prefConfig.readName();

        //Log.e("UserName: ",UserName);
//        textView9=(TextView)view.findViewById(R.id.textView9);

//        textView9.setText("Welcome " + FirstActivity.prefConfig.readName());


        textView10=(TextView)view.findViewById(R.id.textView10);
        thismoney();
        textView14=(TextView)view.findViewById(R.id.textView14);
        textView14.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                Intent intent = new Intent(getActivity(),HistoryActivity.class);
                ((NavigationActivity)getActivity()).startActivityForResult(intent, 1003);
            }
        });

        textView15=(TextView)view.findViewById(R.id.textView15);
        textView15.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                /*
                Fragment fragment = new ViewPayFragment();
                FragmentManager fragmentManager = getFragmentManager();
                FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
                fragmentTransaction.replace(R.id.NavFrag, fragment);
                fragmentTransaction.commit();
                */

                FragmentManager fragmentManager = getFragmentManager();
                fragmentManager.beginTransaction().replace(R.id.NavFrag, new ViewPayFragment()).commit();

            }
        });

        ((NavigationActivity)getActivity()).setActionBarTitle("홈"); //액션바 이름

        // Inflate the layout for this fragment
        return view;
    }

    private void thismoney(){
        TAG_total_fair=0;
        retrofit=new Retrofit.Builder().baseUrl(ROOT_URL).build();
        apiService=retrofit.create(ApiService.class);

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

                        String cardid;
                        String fair;

                        //정수형: getInt(), 실수형: getDouble(), 문자: getString()
                        for(int i=0; i<jsonArray.length(); i++){
                            JSONObject jsonObject=jsonArray.getJSONObject(i);

                            cardid=jsonObject.getString("cardid");
                            fair=jsonObject.getString("fair");

                            Log.v("Test1", jsonObject.toString());
                            //Object 내용 확인: jsonObject.toString()
                            if(cardid.equals(TAG_cardid)){

                                TAG_total_fair +=Integer.parseInt(fair);
                                Log.v("TAG_total_fair", String.valueOf(TAG_total_fair));
                            }
                            textView10.setText(Integer.toString(TAG_total_fair));
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
