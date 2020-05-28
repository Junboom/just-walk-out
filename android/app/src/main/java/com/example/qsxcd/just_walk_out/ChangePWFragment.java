package com.example.qsxcd.just_walk_out;


import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.NavigationView;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;


/**
 * A simple {@link Fragment} subclass.
 */
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import static com.example.qsxcd.just_walk_out.MainActivity.apiService;
import static com.example.qsxcd.just_walk_out.MainActivity.prefConfig;
import static com.example.qsxcd.just_walk_out.NavigationActivity.TAG_email;

public class ChangePWFragment extends Fragment {
    EditText CurrentPW, NewPW, NewPWC;
    Button button_change;
    //public static ApiService apiInterface;

    public ChangePWFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        final View view=inflater.inflate(R.layout.fragment_change_pw, container, false);
        ((NavigationActivity)getActivity()).setActionBarTitle("비밀번호 변경"); //액션바 이름

        CurrentPW=(EditText)view.findViewById(R.id.CurrentPW);
        NewPW=(EditText)view.findViewById(R.id.NewPW);
        NewPWC=(EditText)view.findViewById(R.id.NewPWC);

        button_change=(Button) view.findViewById(R.id.button_change);
        button_change.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                //changPWListener.ChangePW(TAG_email,TAG_password,NewPW.getText().toString());
                performChangePW();
                //performLogin();
            }
        });

        // Inflate the layout for this fragment
        return view;
    }

    private void performChangePW(){
        String Currentpass=CurrentPW.getText().toString();
        String NPW= NewPW.getText().toString();

        if(validar()){
            Log.e("validar", String.valueOf(validar()));
            Log.e("TAG_email",TAG_email);
            Log.e("Currentpass",Currentpass);
            Log.e("changepw",NPW);

            Call<User> call=apiService.performUserPW(TAG_email,Currentpass,NPW);
            call.enqueue(new Callback<User>() {
                @Override
                public void onResponse(Call<User> call, Response<User> response) {

                    Log.e("response: ",response.body().getResponse());

                    if(response.body().getResponse().equals("ok")){
                        Log.e("change","Ok");
                        prefConfig.displayToast("비밀번호 변경에 성공하였습니다.");
                        CurrentPW.setText("");
                        NewPW.setText("");
                        NewPWC.setText("");
                    }else if(response.body().getResponse().equals("failed")){
                        Log.e("change","Failed");
                        prefConfig.displayToast("비밀번호 변경에 실패하였습니다.");
                    }else if(response.body().getResponse().equals("incorrect")){
                        Log.e("change","incorrect");
                        prefConfig.displayToast("비밀번호가 일치하지 않습니다.");
                        NewPWC.setText("");
                    }
                }

                @Override
                public void onFailure(Call<User> call, Throwable t) {
                    Log.e("change","onFailure");
                    prefConfig.displayToast("통신 실패");
                }
            });

        }else{
            Log.e("validar: ", String.valueOf(validar()));
        }
    }

    private boolean validar() {
        boolean valid = true;

        String Currentpass=CurrentPW.getText().toString();
        String Newpass=NewPW.getText().toString();
        String NewpassC=NewPWC.getText().toString();

        if (Currentpass.isEmpty() || Currentpass.length() < 6 || Currentpass.length() > 10) {
            CurrentPW.setError("6~10자리의 비밀번호를 입력해주세요.");
            //LoginActivity.prefConfig.displayToast("6~10자리의 비밀번호를 입력해주세요.");
            valid = false;
        }else{
            CurrentPW.setError(null);
        }
        if (Newpass.isEmpty() || Newpass.length() < 6 || Newpass.length() > 10) {
            NewPW.setError("6~10자리의 비밀번호를 입력해주세요.");
            //LoginActivity.prefConfig.displayToast("6~10자리의 비밀번호를 입력해주세요.");
            valid = false;
        }else{
            NewPW.setError(null);
        }
        if (!NewpassC.equals(Newpass)) {
            NewPWC.setError("비밀번호가 일치하지 않습니다.");
            //LoginActivity.prefConfig.displayToast("비밀번호가 일치하지 않습니다.");
            valid = false;
        }else{
            NewPWC.setError(null);
        }
        return valid;
    }
}
