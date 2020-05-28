package com.example.qsxcd.just_walk_out;

/**
 * Created by qsxcd on 2018-05-13.
 */
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ApiClient {
    //public static final String BASE_URL="http://10.0.2.2/logintest/";
    public static final String BASE_URL="http://54.85.63.115/";

    public static Retrofit retrofit=null;

    public static Retrofit getApiClient(){
        if(retrofit==null){
            retrofit=new Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build();
        }
        return retrofit;
    }
}
