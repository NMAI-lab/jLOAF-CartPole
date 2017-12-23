package CaseBaseCreation;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

import org.jLOAF.casebase.Case;
import org.jLOAF.casebase.CaseBase;
import org.jLOAF.inputs.AtomicInput;
import org.jLOAF.inputs.Feature;
import org.jLOAF.sim.AtomicSimilarityMetricStrategy;
import org.jLOAF.sim.ComplexSimilarityMetricStrategy;
import org.jLOAF.sim.StateBasedSimilarity;
import org.jLOAF.sim.StateBased.KOrderedSimilarity;
import org.jLOAF.sim.atomic.EuclideanDistance;
import org.jLOAF.sim.complex.Mean;

import AgentModules.MCAction;
import AgentModules.MCInput;

public class LogFile2CaseBase {
	
	public void logParser(String logfile, String outfile) throws IOException {
		AtomicSimilarityMetricStrategy Atomic_strat = new EuclideanDistance();
		ComplexSimilarityMetricStrategy complex_strat = new Mean();
		StateBasedSimilarity stateBasedSim = new KOrderedSimilarity(1);
		
		MCInput mcinput;
		MCAction action;
		
		CaseBase cb = new CaseBase();
		
		BufferedReader br = new BufferedReader(new FileReader(logfile),'r');
		String Line;
		String [] input = new String [3];
		System.out.println("Creating casebase...");
		while ((Line = br.readLine()) != null){
			mcinput = new MCInput("Observation",complex_strat);
			
			input = Line.split(",");
			
			mcinput.add(new AtomicInput("x",new Feature(Double.parseDouble(input[0])),Atomic_strat));
			mcinput.add(new AtomicInput("y",new Feature(Double.parseDouble(input[0])),Atomic_strat));
			action = new MCAction(input[2]);
			
			cb.createThenAdd(mcinput, action, stateBasedSim);	
		}
		
		System.out.println("CaseBase created.");
		br.close();
		System.out.println("Writing to file: " + outfile);
		CaseBase.save(cb, outfile);
		System.out.println("Done!");
	}
}
