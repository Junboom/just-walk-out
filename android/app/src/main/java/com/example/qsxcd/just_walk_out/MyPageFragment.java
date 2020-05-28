package com.example.qsxcd.just_walk_out;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

//import static com.example.qsxcd.just_walk_out.LoginActivity.UserEmail;
/**
 * A simple {@link Fragment} subclass.
 */

import static com.example.qsxcd.just_walk_out.NavigationActivity.TAG_name;
import static com.example.qsxcd.just_walk_out.NavigationActivity.TAG_email;
import static com.example.qsxcd.just_walk_out.NavigationActivity.TAG_birth;
import static com.example.qsxcd.just_walk_out.NavigationActivity.TAG_phone;
import static com.example.qsxcd.just_walk_out.NavigationActivity.TAG_cardid;

public class MyPageFragment extends Fragment {

    TextView changepwfrag, main_name, myrfid, myemail, myphone, mybirth, myname;
    static String N;
    static String E;

    public MyPageFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        ((NavigationActivity)getActivity()).setActionBarTitle("내 정보 관리"); //액션바 이름

        View view=inflater.inflate(R.layout.fragment_my_page, container, false);

        main_name=(TextView)view.findViewById(R.id.main_name);
        main_name.setText(TAG_name);
        myrfid=(TextView)view.findViewById(R.id.myrfid);
        myrfid.setText(TAG_cardid);
        myemail=(TextView)view.findViewById(R.id.myemail);
        myemail.setText(TAG_email);
        myphone=(TextView)view.findViewById(R.id.myphone);
        myphone.setText(TAG_phone);
        mybirth=(TextView)view.findViewById(R.id.mybirth);
        mybirth.setText(TAG_birth);
        myname=(TextView)view.findViewById(R.id.myname);
        myname.setText(TAG_name);

        changepwfrag=(TextView)view.findViewById(R.id.changepwfrag);
        changepwfrag.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){

                FragmentManager fragmentManager = getFragmentManager();
                fragmentManager.beginTransaction().replace(R.id.NavFrag, new ChangePWFragment()).commit();

            }
        });

        // Inflate the layout for this fragment
        return view;
    }

}
