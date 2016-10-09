import java.sql.DriverManager;

import com.mysql.jdbc.Connection;
import java.sql.SQLException;

public class migrate {
	public static void main(String[] args){
		
		Connection con = null;
		try{
			con = (Connection) DriverManager.getConnection("jdbc:mysql://wfeinstance.chqag5srs91z.us-west-2.rds.amazonaws.com:3306/wfedb", "WfeMasterUser", "WfeInstance");
			if (con != null){
				System.out.println("Connection Successful");
			}
		} catch (SQLException e){
			System.out.println("Connection Failed. Error: " + e);
		}
	}
}
