#hex_rtt {
  line-color:#51973f;
  line-width:0.5;
  polygon-opacity:.75;
  [rtt_average > 200000]{
	  polygon-fill:#2b8e00;
    }  
  [rtt_average > 100000][rtt_average <= 200000]{
	  polygon-fill:#4ea429;
    }
  [rtt_average > 50000][rtt_average <= 100000]{
	  polygon-fill:#41db00;
    }  
   [rtt_average <= 50000]{
	  polygon-fill:#92ed6b;
    }   
}
