package com.example.statusapp;

import android.app.Activity;
import android.os.Bundle;

public class StatusActivity extends Activity {
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		if (savedInstanceState == null) {
			
			// Create a fragment
			StatusFragment fragment = new StatusFragment();
			getFragmentManager().beginTransaction().add(android.R.id.content, 
						fragment, fragment.getClass().getSimpleName()).commit();
			
		}
	}
}
