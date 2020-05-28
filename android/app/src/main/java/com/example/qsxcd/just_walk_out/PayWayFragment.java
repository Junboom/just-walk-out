package com.example.qsxcd.just_walk_out;


import android.os.Bundle;
import android.support.design.widget.NavigationView;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import static com.example.qsxcd.just_walk_out.MainActivity.ROOT_URL;
import static com.example.qsxcd.just_walk_out.MainActivity.apiService;
import static com.example.qsxcd.just_walk_out.MainActivity.prefConfig;
import static com.example.qsxcd.just_walk_out.PayFragment.TAG_bank_name;
import static com.example.qsxcd.just_walk_out.PayFragment.TAG_account_num;

/**
 * A simple {@link Fragment} subclass.
 */
import static com.example.qsxcd.just_walk_out.NavigationActivity.TAG_cardid;

public class PayWayFragment extends Fragment {

    Button changebtn, cancelhome;

    TextView ac_num, bank;
    EditText new_bank, new_ac_num, new_ac_holder, new_reg_num;

    public PayWayFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment_pay_way, container, false);

        ac_num=(TextView) view.findViewById(R.id.ac_num);
        bank=(TextView) view.findViewById(R.id.bank);
        new_bank=(EditText) view.findViewById(R.id.new_bank);
        new_ac_num=(EditText) view.findViewById(R.id.new_ac_num);
        new_ac_holder=(EditText) view.findViewById(R.id.new_ac_holder);
        new_reg_num=(EditText) view.findViewById(R.id.new_reg_num);

        ac_num.setText(TAG_account_num);
        bank.setText(TAG_bank_name);

        changebtn=(Button) view.findViewById(R.id.changebtn);
        changebtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                performBankInfo();
            }
        });

        cancelhome=(Button) view.findViewById(R.id.cancelhome);
        cancelhome.setOnClickListener(new View.OnClickListener(){
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
                fragmentManager.beginTransaction().replace(R.id.NavFrag, new PayFragment()).commit();

            }
        });

        // Inflate the layout for this fragment
        return view;
    }

    public void performBankInfo(){

        String bank=new_bank.getText().toString();
        String acnum= new_ac_num.getText().toString();
        String acholder=new_ac_holder.getText().toString();
        String regnum= new_reg_num.getText().toString();

        if(validar()){
            Log.e("performBankInfo_validar", String.valueOf(validar()));
            Log.e("bank",bank);
            Log.e("acnum",acnum);
            Log.e("acholder",acholder);
            Log.e("regnum",regnum);

            Call<User> call=apiService.performBankInf(TAG_cardid,bank,acnum,acholder,regnum);
            call.enqueue(new Callback<User>() {
                @Override
                public void onResponse(Call<User> call, Response<User> response) {
                    Log.e("response: ",response.body().getResponse());

                    if(response.body().getResponse().equals("ok")){
                        Log.e("change","Ok");
                        prefConfig.displayToast("요금 납부 정보 변경에 성공하였습니다.");
                        new_bank.setText("");
                        new_ac_num.setText("");
                        new_ac_holder.setText("");
                        new_reg_num.setText("");
                    }else if(response.body().getResponse().equals("failed")){
                        Log.e("change","Failed");
                        prefConfig.displayToast("요금 납부 정보 변경에 실패하였습니다.");
                    }
                }
                @Override
                public void onFailure(Call<User> call, Throwable t) {
                    Log.e("change","onFailure");
                    prefConfig.displayToast("통신 실패");
                }
            });

        }else{
            Log.e("performBankInfo_validar", String.valueOf(validar()));
        }
    }

    private boolean validar() {
        boolean valid = true;

        String bank=new_bank.getText().toString();
        String acnum= new_ac_num.getText().toString();
        String acholder=new_ac_holder.getText().toString();
        String regnum= new_reg_num.getText().toString();

        if (bank.isEmpty()) {
            new_bank.setError("은행 이름을 입력해주세요.");
            valid = false;
        }else{
            new_bank.setError(null);
        }
        if (acnum.isEmpty()) {
            new_ac_num.setError("계좌번호를 입력해주세요.");
            valid = false;
        }else{
            new_ac_num.setError(null);
        }
        if (acholder.isEmpty()) {
            new_ac_holder.setError("예금주 이름을 입력해주세요.");
            valid = false;
        }else{
            new_ac_holder.setError(null);
        }
        if (regnum.isEmpty()) {
            new_reg_num.setError("주민등록번호를 입력해주세요.");
            valid = false;
        }else{
            new_reg_num.setError(null);
        }
        return valid;
    }
}
