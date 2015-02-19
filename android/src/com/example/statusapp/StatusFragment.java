package com.example.statusapp;

import android.app.Fragment;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.AsyncTask;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.os.Bundle;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;

import android.view.Menu;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.marakana.android.yamba.*;
import com.marakana.android.yamba.clientlib.YambaClient;
import com.marakana.android.yamba.clientlib.YambaClientException;

@SuppressWarnings("unused")
public class StatusFragment extends Fragment implements OnClickListener {
	private static final String TAG = "StatusFragment ";
	private EditText editStatus;
	private Button buttonTweet;
	private TextView textCount;  
	private int defaultTextColor;
	
	SharedPreferences prefs;
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		View view = inflater.inflate(R.layout.fragment_status, container, false);
	
		// Hook up Variables
		editStatus = (EditText) view.findViewById(R.id.editStatus);
		buttonTweet = (Button) view.findViewById(R.id.buttonTweet);		
		textCount = (TextView) view.findViewById(R.id.textCount);
		buttonTweet.setOnClickListener(this);
		
		defaultTextColor = textCount.getTextColors().getDefaultColor();
		
		editStatus.addTextChangedListener(new TextWatcher() {

			@Override
			public void afterTextChanged(Editable s) {
				int count = 140 - editStatus.length(); // 
				textCount.setText(Integer.toString(count));
				textCount.setTextColor(Color.GREEN); // 
				if (count < 10)
					textCount.setTextColor(Color.RED);
				else
					textCount.setTextColor(defaultTextColor);
			}

			@Override
			public void beforeTextChanged(CharSequence s, int start,
					int count, int after) {
				// TODO Auto-generated method stub
				
			}

			@Override
			public void onTextChanged(CharSequence s, int start, int count,
					int after) {
				// TODO Auto-generated method stub
			}
			
		});
		
		return view;
	}

	@Override
	public void onClick(View v) {
		String Status = editStatus.getText().toString();
		Log.d(TAG, "OnClick with Status" + Status);
		new PostTask().execute(Status);
	}
	
	private final class PostTask extends AsyncTask <String, Void, String > {

		@Override
		protected String doInBackground(String... arg0) 
		{
			YambaClient YambaCloud = new YambaClient("student", "password");
			try {
				YambaCloud.postStatus(arg0[0]);
				return "Posted Successfully";
			}
			catch (YambaClientException e) {
				e.printStackTrace();
				return "Failed to Post";
			}
		}
		
		@Override
		protected void onPostExecute(String result) 
		{
			super.onPostExecute(result);
			Toast.makeText(StatusFragment.this.getActivity(), result, Toast.LENGTH_LONG).show();
	    }
	}
}