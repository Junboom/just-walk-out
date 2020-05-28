package com.example.qsxcd.just_walk_out;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.POST;
import retrofit2.http.Field;

/**
 * Created by qsxcd on 2018-04-13.
 */

public interface ApiService {

    //public static final String API_URL="http://34.207.213.77/recordsgetjson.php/";
/*
    @FormUrlEncoded
    @POST("/signup.php")
    public void insertUser(
            @Field("name") String name,
            @Field("email") String email,
            @Field("password") String password,
            @Field("birth") String birth,
            @Field("phone") String phone,
            @Field("rfid") String rfid,
            Callback<Response> callback);

    @FormUrlEncoded
    @POST("/login.php")
    public void loginUser(
            @Field("email") String email,
            @Field("password") String password,
            Callback<Response> callback);
*/

    @FormUrlEncoded
    @POST("register.php")
    Call<User> performRegistration(@Field("name") String Name,
                                   @Field("email") String Email,
                                   @Field("password") String Password,
                                   @Field("birth") String Birth,
                                   @Field("phone") String Phone,
                                   @Field("rfid") String Rfid);

    @FormUrlEncoded
    @POST("login.php")
    Call<User> performUserLogin(@Field("email") String Email,
                                @Field("password") String Password);

    @FormUrlEncoded
    @POST("changepw.php")
    Call<User> performUserPW(@Field("email") String Email,
                             @Field("password") String Password,
                             @Field("changepw") String Changepw);

    @FormUrlEncoded
    @POST("changebank.php")
    Call<User> performBankInf(@Field("rfid_id") String rfid_id,
                              @Field("bank_name") String bank_name,
                              @Field("account_num") String account_num,
                              @Field("acc_holder") String acc_holder,
                              @Field("regist_num") String regist_num);

    @FormUrlEncoded
    @POST("recordsgetjson.php")
    Call<ResponseBody> getPostrecord(@Field("id") String id);

    @FormUrlEncoded
    @POST("selectUser.php")
    Call<ResponseBody> getPostuser(@Field("email") String email);

    @FormUrlEncoded
    @POST("banksgetjson.php")
    Call<ResponseBody> getPostBank(@Field("rfid_id") String rfid_id);

}
