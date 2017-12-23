package AgentModules;

import org.jLOAF.Agent;
import org.jLOAF.MotorControl;
import org.jLOAF.Perception;
import org.jLOAF.Reasoning;
import org.jLOAF.action.Action;
import org.jLOAF.casebase.CaseBase;
import org.jLOAF.inputs.Input;

public class MCAgent extends Agent {

	public MCAgent() {
		super(null, null, null, null);
		
	}

	@Override
	public Action run(Input i) {
		// TODO Auto-generated method stub
		return this.r.selectAction(i);
	}

}
