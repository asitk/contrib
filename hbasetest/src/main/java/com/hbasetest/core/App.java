package com.hbasetest.core;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.util.Bytes;

/**
 * Hello world!
 *
 */
public class App 
{
	private static final String strlog4jConfigFile = "/src/log4j.properties";
	private static final Logger Log = Logger.getLogger("GLOBAL");
	
	public static final String HBASE_CONFIGURATION_ZOOKEEPER_QUORUM                     = "localhost";
	public static final String HBASE_CONFIGURATION_ZOOKEEPER_CLIENTPORT                 = "2181";
	
	/**
	 * Prints usage 
	 */
	@SuppressWarnings("unused")
	private static void Usage() {
		System.out.println("Usage: ");
		System.out.println("./target/appassembler/bin/hbasetest");
	}
	
	/**
	 * Initiatizes logging
	 */
    private static void InitLogger()
    {
    	try {
    		String workingDir = System.getProperty("user.dir");
    		FileInputStream in;
			in = new FileInputStream(workingDir + strlog4jConfigFile);
		   	Properties props = new Properties();
	   		props.load(in);
	   		PropertyConfigurator.configure(props);
    	}
 	   	catch (Exception e) {
			e.printStackTrace();
			System.exit(0);
		}
    }

    public static void main( String[] args )
    {
    	InitLogger();
		Log.info("Init");
		
		Configuration hBaseConfig =  HBaseConfiguration.create();
	    hBaseConfig.setInt("timeout", 120000);
	    hBaseConfig.set("hbase.master", "127.0.0.1:60000");
	    hBaseConfig.set("hbase.zookeeper.quorum", "127.0.0.1");
	    hBaseConfig.set("hbase.zookeeper.property.clientPort", "2181");
	    
	    try {
			HBaseAdmin admin = new HBaseAdmin(hBaseConfig);
			
			if (!admin.tableExists("people")) {
				HTableDescriptor tableDescriptor = new HTableDescriptor("people");
				tableDescriptor.addFamily(new HColumnDescriptor("personal"));
				tableDescriptor.addFamily(new HColumnDescriptor("contactinfo"));
				tableDescriptor.addFamily(new HColumnDescriptor("creditcard"));
				admin.createTable(tableDescriptor);
				admin.close();
			}
			
			HTable table = new HTable(hBaseConfig, "people");
			Put put = new Put(Bytes.toBytes("doe-john-m-12345"));
			put.add(Bytes.toBytes("personal"), Bytes.toBytes("givenName"), Bytes.toBytes("John"));
			put.add(Bytes.toBytes("personal"), Bytes.toBytes("mi"), Bytes.toBytes("M"));
			put.add(Bytes.toBytes("personal"), Bytes.toBytes("surame"), Bytes.toBytes("Doe"));
			put.add(Bytes.toBytes("contactinfo"), Bytes.toBytes("email"), Bytes.toBytes("john.m.doe@gmail.com"));
			table.put(put);
			table.flushCommits();
			table.close();
		
		}
	    catch (MasterNotRunningException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ZooKeeperConnectionException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	    catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}	    
   }
}
