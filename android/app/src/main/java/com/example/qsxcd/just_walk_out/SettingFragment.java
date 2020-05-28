package com.example.qsxcd.just_walk_out;


import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v7.app.AlertDialog;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.CompoundButton.OnCheckedChangeListener;



/**
 * A simple {@link Fragment} subclass.
 */

import static com.example.qsxcd.just_walk_out.MainActivity.prefConfig;
import static com.example.qsxcd.just_walk_out.NavigationActivity.TAG_email;

public class SettingFragment extends Fragment {
    TextView mypageTextbtn, logoutTextbtn, Useremail;
    Switch autoLoginSwitch;

    public SettingFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        ((NavigationActivity)getActivity()).setActionBarTitle("설정"); //액션바 이름

        final View view=inflater.inflate(R.layout.fragment_setting, container, false);

        Useremail=(TextView)view.findViewById(R.id.Useremail);

        autoLoginSwitch=view.findViewById(R.id.autoLoginSwitch);

        mypageTextbtn = (TextView) view.findViewById(R.id.mypageTextbtn);


        Log.e("num",prefConfig.readNum());
        if(prefConfig.readNum().equals("0")){
            Log.e("0","자동로그인");
            prefConfig.writeNum("0");
            autoLoginSwitch.setChecked(true);
        }else if(prefConfig.readNum().equals("1")){
            Log.e("1","일반로그인");
            prefConfig.writeNum("1");
            autoLoginSwitch.setChecked(false);
        }

        Useremail.setText(TAG_email);
        autoLoginSwitch.setOnCheckedChangeListener(new OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                if(b){//스위치ON(자동로그인)
                    Log.e("autoLoginSwitch","자동로그인 설정");
                    prefConfig.writeLoginStatus(true);
                    prefConfig.writeNum("0");
                }else{//스위치OFF
                    Log.e("autoLoginSwitch","자동로그인 설정 취소");
                    prefConfig.writeLoginStatus(false);
                    prefConfig.writeNum("1");
                }
            }
        });
                mypageTextbtn.setOnClickListener(new View.OnClickListener(){
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
                fragmentManager.beginTransaction().replace(R.id.NavFrag, new MyPageFragment()).commit();

            }
        });

        logoutTextbtn=(TextView) view.findViewById(R.id.logoutTextbtn);
        logoutTextbtn.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){

                AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
                builder.setTitle("로그아웃").setMessage("로그아웃 하시겠습니까?")
                        .setPositiveButton("로그아웃", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int whichButton) {

                                Intent intent = new Intent(getActivity(),LoginActivity.class);
                                ((NavigationActivity)getActivity()).startActivityForResult(intent, 1005);

                                intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP|Intent.FLAG_ACTIVITY_SINGLE_TOP);
                                startActivity(intent);
                            }
                        })
                        .setNegativeButton("취소", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int whichButton){

                            }
                        }).show();
            }
        });

        ((NavigationActivity)getActivity()).setActionBarTitle("설정"); //액션바 이름

        // Inflate the layout for this fragment
        return view;
    }

}
