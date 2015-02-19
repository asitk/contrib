package com.example.statusapp;

import android.content.SharedPreferences;
import android.content.SharedPreferences.OnSharedPreferenceChangeListener;
import android.os.Bundle;
import android.preference.PreferenceFragment;
import android.preference.PreferenceManager;

public class SettingsFragment extends PreferenceFragment implements
OnSharedPreferenceChangeListener { // 
	private SharedPreferences prefs;
	
	@Override
	public void onCreate(Bundle savedInstanceState) { // 
		super.onCreate(savedInstanceState);
		addPreferencesFromResource(R.xml.settings); // 
	}

	@Override
	public void onStart() {
		super.onStart();
		prefs = PreferenceManager.getDefaultSharedPreferences(getActivity());
		prefs.registerOnSharedPreferenceChangeListener(this);
	}

	@Override
	public void onSharedPreferenceChanged(SharedPreferences arg0, String arg1) {
		// TODO Auto-generated method stub
	}
}