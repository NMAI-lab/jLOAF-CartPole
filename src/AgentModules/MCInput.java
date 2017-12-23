package AgentModules;

import org.jLOAF.inputs.ComplexInput;
import org.jLOAF.sim.ComplexSimilarityMetricStrategy;

public class MCInput extends ComplexInput {
private static final long serialVersionUID = 1L;
	
	public MCInput(String s, ComplexSimilarityMetricStrategy sim) {
		super(s, sim);
	}
}
