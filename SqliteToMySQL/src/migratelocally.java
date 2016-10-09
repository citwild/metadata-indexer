import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import com.mysql.jdbc.Connection;
import java.sql.SQLException;
import java.sql.Statement;

public class migratelocally {
	public static void main(String[] args){
		
		//Connecting to MySQL database
		Connection con = null;
		try{
			con = (Connection) DriverManager.getConnection("jdbc:mysql://localhost:3306/beamcoffermetadata?user=root");
			if (con != null){
				System.out.println("Connection to MySQL Successful");
			}
		} catch (SQLException e){
			System.out.println("Connection to MySQL Failed. Error: " + e);
		}
		
		//Connecting to SQLite database
		java.sql.Connection consqlite = null;
		try{
			Class.forName("org.sqlite.JDBC");
			consqlite = DriverManager.getConnection("jdbc:sqlite:bc_data_v3.db");
			consqlite.setAutoCommit(false);
			if (consqlite != null){
				System.out.println("Connection to SQLite Successful");
			}
		} catch (Exception e){
			System.out.println("Connection to SQLite Failed. " + e.getClass().getName() + ": " + e.getMessage());
		}
		
		//Read data from SQLite database
		Statement readStmt;
		try{
			readStmt = consqlite.createStatement();
			ResultSet rs = readStmt.executeQuery( "SELECT * FROM main;" );
			
			String insertMedia = " insert into media (media_id, media_aws_key, media_type, media_extension, media_sensor, media_sensor_location)"
			        + " values (?, ?, ?, ?, ?, ?)";
			PreparedStatement psMedia = con.prepareStatement(insertMedia);
			
			String insertImage = " insert into picture (media_id, picture_width, picture_height, picture_mtime, picture_date)"
			        + " values (?, ?, ?, ?, ?)";
			PreparedStatement psImage = con.prepareStatement(insertImage);
			
			String insertVideo = " insert into video (media_id, video_width, video_height, video_mtime_begin, video_mtime_end, video_duration, video_date)"
			        + " values (?, ?, ?, ?, ?, ?, ?)";
			PreparedStatement psVideo = con.prepareStatement(insertVideo);
			
			while ( rs.next() ) {
				int media_id = rs.getInt("media_id");
				String file_path = rs.getString("file_path");
				String media_type = rs.getString("media_type");
				int width = rs.getInt("width");
				int height = rs.getInt("height");
				int duration = rs.getInt("duration");
				int mtime_begin = rs.getInt("mtime_begin");
				int mtime_end = rs.getInt("mtime_end");
				String date = rs.getString("nominal_date");
				String sensor = rs.getString("equipment");
				String sensor_location = rs.getString("location");
				String extension = rs.getString("file_ext");
				
				String media_aws_key = file_path.replace("/Volumes/NO NAME/", "beamcoffer/photos/");
				media_aws_key = media_aws_key.replace("/Volumes/NO NAME/analysis/", "beamcoffer/");
				//media_aws_key = media_aws_key.replace(" ", "+");
				System.out.println(media_id);
				
				psMedia.setInt(1, media_id);
				psMedia.setString(2, media_aws_key);
				psMedia.setString(3, media_type);
				psMedia.setString(4, extension);
				psMedia.setString(5, sensor);
				psMedia.setString(6, sensor_location);
				psMedia.execute();
				
				if (media_type.equals("Image")){
					psImage.setInt(1, media_id);
					psImage.setInt(2, width);
					psImage.setInt(3, height);
					psImage.setInt(4, mtime_begin);
					psImage.setString(5, date);
					psImage.execute();
				}
				else{
					psVideo.setInt(1, media_id);
					psVideo.setInt(2, width);
					psVideo.setInt(3, height);
					psVideo.setInt(4, mtime_begin);
					psVideo.setInt(5, mtime_end);
					psVideo.setInt(6, duration);
					psVideo.setString(7, date);
					psVideo.execute();
				}
			}
			
			rs.close();
			readStmt.close();
		    consqlite.close();
		    
		}catch(Exception e){
			System.out.println( "Operations Failed. " + e.getClass().getName() + ": " + e.getMessage() );
		}
		
	}
}