package com.mr.core;

import java.io.IOException;
import java.util.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class MappersAndReducers {

	 public static class WordMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
		 private final static IntWritable one = new IntWritable(1);
		 private Text word = new Text();
		 
		 public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			 String line = value.toString();
			 StringTokenizer tokenizer = new StringTokenizer(line);
			 while (tokenizer.hasMoreTokens()) {
				 word.set(tokenizer.nextToken());
				 System.out.println("map: " + word.toString());
				 context.write(word, one);
			 }
		 }
	 }
	
	 public static class WordSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {

		 public void reduce(Text key, Iterable<IntWritable> it, Context context)
				throws IOException, InterruptedException {
			 	int sum = 0;
		 		System.out.println("Reduce");				 	
		 		Iterator<IntWritable> values = it.iterator();
		 		while ((values).hasNext()) {
			 		sum += (values).next().get();
			 		System.out.println("Sum" + Integer.toString(sum));				 	
			 	}
			 	context.write(key, new IntWritable(sum));
		 }
	 }
	 
	 public static class TempMapper extends Mapper <LongWritable, Text, Text, IntWritable> {
		 
		 public void map(LongWritable Key, Text value, Context context) throws IOException, InterruptedException {
			 String line = value.toString();
			 String Year = line.substring(0, 4);			 
			 int Temp = Integer.parseInt(line.substring(5, line.length()));			 
			 context.write(new Text(Year), new IntWritable(Temp));	
		 }
	 }
	 
	 public static class TempReducer extends Reducer<Text, IntWritable, Text, IntWritable> {

		 public void reduce(Text Key, Iterable<IntWritable>Temps, Context context) throws IOException, InterruptedException {
			 int maxValue = Integer.MIN_VALUE;
			 for (IntWritable Temp : Temps) {
				 maxValue = Math.max(maxValue, Temp.get());
			 }
			 context.write(Key, new IntWritable(maxValue));
		 }
	 }
	
	 public static void main(String[] args) throws Exception {
		 Configuration conf = new Configuration();
		 
		 //Job job = new Job(conf, "WordCount");
		 //job.setJarByClass(MappersAndReducers.class);
		 //job.setOutputKeyClass(Text.class);
		 //job.setOutputValueClass(IntWritable.class);
		 //job.setMapperClass(MappersAndReducers.WordMapper.class);
		 //job.setCombinerClass(MappersAndReducers.WordSumReducer.class);
		 //job.setReducerClass(MappersAndReducers.WordSumReducer.class);
		 //job.setInputFormatClass(TextInputFormat.class);
		 //job.setOutputFormatClass(TextOutputFormat.class);
		 //FileInputFormat.addInputPath(job, new Path(args[0]));
		 //FileOutputFormat.setOutputPath(job, new Path(args[1]));
		 
		 Job job = new Job(conf, "MaxTemp");
		 job.setJarByClass(MappersAndReducers.class);
		 job.setOutputKeyClass(Text.class);
		 job.setOutputValueClass(IntWritable.class);
		 job.setMapperClass(MappersAndReducers.TempMapper.class);
		 job.setCombinerClass(MappersAndReducers.TempReducer.class);
		 job.setReducerClass(MappersAndReducers.TempReducer.class);
		 job.setInputFormatClass(TextInputFormat.class);
		 job.setOutputFormatClass(TextOutputFormat.class);
		 FileInputFormat.addInputPath(job, new Path(args[0]));
		 FileOutputFormat.setOutputPath(job, new Path(args[1]));
		 
		 job.waitForCompletion(true);
		 
		 System.out.println("Done");
	 }
}
