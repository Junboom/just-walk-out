package com.example.qsxcd.just_walk_out;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;


/**
 * A simple {@link Fragment} subclass.
 */
public class CustomerSupportFragment extends Fragment {


    public CustomerSupportFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        ((NavigationActivity)getActivity()).setActionBarTitle("고객 센터"); //액션바 이름
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_customer_support, container, false);
    }

}
