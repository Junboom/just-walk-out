package com.example.qsxcd.just_walk_out;


import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;


/**
 * A simple {@link Fragment} subclass.
 */
public class ViewPayFragment extends Fragment {
    TextView textView16;

    public ViewPayFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        View view=inflater.inflate(R.layout.fragment_view_pay, container, false);

        textView16=(TextView)view.findViewById(R.id.textView16);
        textView16.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                FragmentManager fragmentManager = getFragmentManager();
                fragmentManager.beginTransaction().replace(R.id.NavFrag, new PayFragment()).commit();
            }
        });

        ((NavigationActivity)getActivity()).setActionBarTitle("요금 조회 및 납부"); //액션바 이름
        // Inflate the layout for this fragment
        return view;
    }
}
