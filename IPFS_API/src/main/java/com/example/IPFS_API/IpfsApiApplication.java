package com.example.IPFS_API;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class IpfsApiApplication {

	 public static void main(String[] args) {
		SpringApplication.run(IpfsApiApplication.class, args);
		 System.out.println("in upload") ;
	 }

	/*public static void main(String[] args) {
		SpringApplication.run(com.example.ipfsdemon.IpfsDemonApplication.class, args);
	}*/

}
