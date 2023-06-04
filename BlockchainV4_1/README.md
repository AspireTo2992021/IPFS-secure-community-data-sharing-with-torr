# Blockchain-Voting-System

A.	Materials/Components/Flowchart/Block Diagram/Theory



  


B.	Components

●	
Flask
●	Javascript 
●	Pyzbar.pyzbar
●	Crypto.py for RSA , SHA256, Signature 
●	Urllib to parse url


C.	Pseudo-Random Consensus Algorithm
		
		In the proposed model, we are trying to achieve a consensus model which minimizes the possibility of any sort of self-interest taking over the fairness and reliability of the election. If the nodes and hence the owners of the nodes are completely stripped away of any self interest, then and only then will such a model be fair. To achieve this we had to look into the shortcomings of POW (Proof-of-work) and POS (Proof-of-Stake) consensus.
Here, we have proposed a method that randomly assigns the consensus to a node. This assures that in a specific period of time, there is no way to possibly rig the data entry of a block. The algorithm generates random sequence of numbers which is then used to identify which node will put the data into the file. A random seed is used for attempt 0 then the output of attempt zero becomes the seed for attempt 1 and so on.
This way we are able to achieve complete random reliance, at least for a specific limited amount of time which is ideal for our use case as we can use a specific chain for a specific election and hence the lifetime of the chain’s data mining has to be limited. 



1.	RESULT


A.	 Frontend (Voting page)


 
B.	Frontend (Eligibility check)
	
 


C.	
  

