package com.example.qsxcd.just_walk_out;

import com.google.gson.annotations.SerializedName;

/**
 * Created by qsxcd on 2018-05-13.
 */

public class User {
    @SerializedName("response")
    private String Response;

    @SerializedName("name")
    private String Name;

    @SerializedName("email")
    private String Email;

    public String getResponse(){
        return Response;
    }

    public String getName(){
        return Name;
    }

    public String getEmail(){
        return Email;
    }
}
