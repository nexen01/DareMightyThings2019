package web;

import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.realiser.english.*;
import simplenlg.phrasespec.*;

import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import simplenlg.features.*;

public class NarrativeGenerator {
	public static NLGFactory nlgFactory;
	public static Lexicon lexicon;
	public static Realiser realiser;
	public static String[] plabels;
	public static String[] plisting;
	public static String[] alabels;
	public static String[] alisting;
	public static String[] rests;
	public static String[] coffee;
	public static String[] airport;
	public static String[] trainstop;
	public static void main(String[] args) {		
		lexicon = Lexicon.getDefaultLexicon();
		nlgFactory = new NLGFactory(lexicon);
		realiser = new Realiser(lexicon);
		


		
		ArrayList<DocumentElement> narrative = new ArrayList<DocumentElement>();
	  
		plabels = convertArray(args[0]);
	    
	    plisting =  convertArray(args[1]);
	    
	    
	    alabels = convertArray(args[2]);
	    
	    alisting =  convertArray(args[3]);
	    
	    rests = convertArray(args[4]);	    
	    airport = convertArray(args[5]);
	    
	    	    
	    
	    /*
	    System.out.println(alabels.length);
	    for(String s : alabels) {
	    	System.out.println(s);
	    }*/
	    

	    narrative.add(sentence1()); //"Build-To-Suit, Lots 2,3,4" is located at I-90 At Randall Rd @ drn, Elgin Illinois.
	    narrative.add(sentence2()); //It is an Office building in the Northwest sub market of the Chicago market.
	    narrative.add(sentence3()); //"Build-To-Suit, Lots 2,3,4" is a Low-Rise building with 2 floors and an average of "113,450" leasable square feet per floor.
	    narrative.add(sentence4()); //The occupancy rate of "Build-To-Suit, Lots 2,3,4" is 100%
	    narrative.add(sentence5()); //Out of the 100 square feet of office space and 100 square feet of retail space there is 100 square feet available.
	    narrative.add(sentence6()); //The building offers None as amenities.
	    narrative.add(sentence7()); // BuildingName is built in 2020
	    narrative.add(sentence8()); //Bob is the primary owner of "Build-To-Suit, Lots 2,3,4".
	    narrative.add(sentence9()); //The building is leased by CBRE.
	    
		    
	    
	    if(!getPCell("View").equals("None")){
	    	narrative.add(sentence10());	    
	    }
	    
	    narrative.add(sentence11()); //resteraunt.

	    
	    if(airport != null) {
	    	narrative.add(sentence12());
	    }
	    DocumentElement paragraph = nlgFactory.createParagraph(narrative);
	    String output = realiser.realise(paragraph).getRealisation();
	    System.out.println(output);


	}
	public static String[] convertArray(String row){
		
		return row.split("\t");
	}
	public static String getPCell(String varname) {
		String s = "";
		for(int i = 0;i<plabels.length;i++) {
			//System.out.println(labels[i]);
			if(varname.equals(plabels[i].trim())) {
				//System.out.println(i);
				s = plisting[i];
			}
		}
		if(s.equals("nan")) {
			s = "None";
		}
		return s;
	}
	public static String getACell(String varname) {
		String s = "";
		for(int i = 0;i<alabels.length;i++) {
			//System.out.println(labels[i]);
			if(varname.equals(alabels[i].trim())) {
				//System.out.println(i);
				s = alisting[i];
			}
		}
		if(s.equals("nan")) {
			s = "None";
		}
		return s;
	}
	public static DocumentElement sentence1() {
		SPhraseSpec p = nlgFactory.createClause();
		p.setSubject(getPCell("Bldg Name"));
		p.setVerb("is located");    	
		String address = getPCell("Address") + ", " + getPCell("City") + " " + getPCell("State");
		NPPhraseSpec place = nlgFactory.createNounPhrase(address);
		
		PPPhraseSpec pp = nlgFactory.createPrepositionPhrase();
		pp.setPreposition("at");
		pp.addComplement(place);    
		
		p.addComplement(pp);
		
		

		if(!getACell("Availability Type").equals("None")) {
			SPhraseSpec sp = nlgFactory.createClause();
			PPPhraseSpec pp1 = nlgFactory.createPrepositionPhrase();
		    VPPhraseSpec vp = nlgFactory.createVerbPhrase(); 
			NPPhraseSpec np= nlgFactory.createNounPhrase(); 

			vp.setVerb("is");
			vp.setObject(pp1);
			
			pp1.setPreposition("for");
			pp1.setObject(np);
			pp1.setPreModifier("available");
			np.setNoun("lease");
			CoordinatedPhraseElement c = nlgFactory.createCoordinatedPhrase();		    
		    c.addCoordinate(p);
		    c.addCoordinate(vp);
			return nlgFactory.createSentence(c);

		}
		else {
			return nlgFactory.createSentence(p);
		}
		
	}
	public static DocumentElement sentence2() {
		SPhraseSpec sp = nlgFactory.createClause();
		
	    NPPhraseSpec np= nlgFactory.createNounPhrase(); 
	    NPPhraseSpec np1= nlgFactory.createNounPhrase(); 
	    NPPhraseSpec np2= nlgFactory.createNounPhrase(); 

	    PPPhraseSpec pp1 = nlgFactory.createPrepositionPhrase();
	    PPPhraseSpec pp2 = nlgFactory.createPrepositionPhrase();

	    VPPhraseSpec vp1= nlgFactory.createVerbPhrase(); 

	    String type = getPCell("Bldg Type");
	    String subtype = getPCell("Building Sub Type");    
	    
	    sp.setSubject("it");
	    
	    vp1.setVerb("is");
	    
	
	    np.setSpecifier("a");
	    
	    if(type.equals(subtype)) {
	    	 np.setNoun(type+ " building");
	    }
	    else {
	    	 np.setNoun(subtype + " " + type + " building");
	    }
	    
	    pp1.setComplement(np1);
	    pp1.setPreposition("in");
	    
	    np1.setNoun(getPCell("Submarket") + " sub market");
	    np1.setSpecifier("the");
	    
	    pp2.setComplement(np2);
	    pp2.setPreposition("of");
	    
	    
	    np2.setNoun(getPCell("Market") + " market");
	    np2.setSpecifier("the");
	    
	    
	    
	   	sp.setVerbPhrase(vp1);
	   	sp.setComplement(np);
	   	sp.setComplement(pp1);
	   	sp.setComplement(pp2);
	   	
		return nlgFactory.createSentence(sp);
	}
	public static DocumentElement sentence3() {
		SPhraseSpec sp = nlgFactory.createClause();
		SPhraseSpec sp1 = nlgFactory.createClause();

	    NPPhraseSpec np= nlgFactory.createNounPhrase(); 
	    NPPhraseSpec np1= nlgFactory.createNounPhrase(); 
	    NPPhraseSpec np2= nlgFactory.createNounPhrase(); 
	    NPPhraseSpec np3= nlgFactory.createNounPhrase(); 
	    
	    PPPhraseSpec pp1 = nlgFactory.createPrepositionPhrase();
	    PPPhraseSpec pp2 = nlgFactory.createPrepositionPhrase();
	    PPPhraseSpec pp3 = nlgFactory.createPrepositionPhrase();

	    VPPhraseSpec vp1= nlgFactory.createVerbPhrase(); 
	    
	    sp.setSubject(getPCell("Bldg Name"));
	    sp.setVerb("is");
	    sp.setObject(np);
	    
	    
	    np.setNoun("building");
	    np.setSpecifier("a");
	    np.setPreModifier(getPCell("Story Type"));
	    
	    pp1.setPreposition("with");
	    pp1.setComplement(np1);
	    
	    
	    np1.setNoun("floor");
	    np1.setPreModifier(getPCell("Stories"));
	    np1.setFeature(Feature.NUMBER, NumberAgreement.PLURAL);
	    
	    vp1.setVerb("is");
	    vp1.addFrontModifier("also");
	    vp1.setObject(np);
	    
	    sp.addComplement(pp1);

	    sp1.setObject(np2);

	    
	    np2.setDeterminer("a");
	    np2.setNoun("average");
	    np2.addComplement(pp2);
	    pp2.setPreposition("of");
	    pp2.setObject(np3);
	   

	    //pp2.setComplement(np2);
	    np3.setNoun("square feet");
	    np3.addPreModifier(getPCell("Average Floor Plate Size")+ " leasable");
	    np3.addComplement(pp3);
	    
	    pp3.setPreposition("per");
	    pp3.setObject("floor");
	    //sp.setComplement(vp1);
	    //sp.setComplement(pp1);
	    CoordinatedPhraseElement c = nlgFactory.createCoordinatedPhrase();
	    c.addCoordinate(sp);
	    c.addCoordinate(sp1);
	    
		return nlgFactory.createSentence(c);
	}
	public static DocumentElement sentence4() {
		SPhraseSpec sp = nlgFactory.createClause();
		SPhraseSpec sp1 = nlgFactory.createClause();

	    NPPhraseSpec np= nlgFactory.createNounPhrase(); 
	    NPPhraseSpec np1= nlgFactory.createNounPhrase(); 
	    NPPhraseSpec np2= nlgFactory.createNounPhrase(); 
	    NPPhraseSpec np3= nlgFactory.createNounPhrase(); 
	    
	    PPPhraseSpec pp1 = nlgFactory.createPrepositionPhrase();
	    PPPhraseSpec pp2 = nlgFactory.createPrepositionPhrase();
	    PPPhraseSpec pp3 = nlgFactory.createPrepositionPhrase();

	    VPPhraseSpec vp1= nlgFactory.createVerbPhrase(); 
	    
	    np.setSpecifier("the");
	    np.setNoun("occupancy rate");
	    
	    pp1.setObject(getPCell("Bldg Name"));
		pp1.setPreposition("of");

	    //pp1.addComplement(vp1);

	    vp1.setVerb("is");	    
	    vp1.addPostModifier(getPCell("Occ Rate"));
	    //vp1.addModifier("100%");
	    
	    sp.setObject(np);
	    sp.addComplement(pp1);
	    sp.addComplement(vp1);
	    
		return nlgFactory.createSentence(sp);
	}
	public static DocumentElement sentence5() {
		SPhraseSpec sp = nlgFactory.createClause();
		SPhraseSpec sp1 = nlgFactory.createClause();
		SPhraseSpec sp2 = nlgFactory.createClause();

		NPPhraseSpec np = nlgFactory.createNounPhrase(); 
		NPPhraseSpec np1 = nlgFactory.createNounPhrase(); 
		NPPhraseSpec np2 = nlgFactory.createNounPhrase(); 
		NPPhraseSpec np3 = nlgFactory.createNounPhrase(); 

		PPPhraseSpec pp = nlgFactory.createPrepositionPhrase();
		PPPhraseSpec pp1 = nlgFactory.createPrepositionPhrase();
		PPPhraseSpec pp2 = nlgFactory.createPrepositionPhrase();

		VPPhraseSpec vp= nlgFactory.createVerbPhrase(); 
		
		pp.setPreposition("out of");
		pp.setObject(np);
		
		
		String cell;
		if(getPCell("Office s.f.").equals("None")) {
			cell = "3222";
		}
		else {
			cell=getPCell("Office s.f.");
		}
		
		np.setSpecifier("the");
		//np.addPreModifier("100");
		np.addModifier(cell);
		np.setNoun("square feet");
	    

		
		np.addComplement(pp1);
		pp1.setPreposition("of");
		pp1.setObject(nlgFactory.createNounPhrase("office space"));
		
		/*vp.setVerb("are");
		
		vp.setObject("office space");*/
		sp1.setObject(np1);
		
		np1.setNoun("square feet");
		//np1.addPreModifier("100");
		String cell1;
		if(getPCell("Retail s.f.").equals("None")) {
			cell1 = "2138";
		}
		else {
			cell1=getPCell("Retail s.f.");
		}
		np1.setPreModifier(cell1);
		
		sp1.addComplement(pp2);

		pp2.setPreposition("of");
		pp2.setComplement(np2);
		np2.setNoun("retail space");
        // may revert to nlgFactory.createCoordinatedPhrase( subject1, subject2 ) ;
		
		sp2.setVerb("are");
		sp2.addFrontModifier("there");
		sp2.setObject(np3);
		np3.setNoun("square feet");
		np3.setPreModifier(getPCell("Available s.f."));
		np3.setPostModifier("available");
		CoordinatedPhraseElement c = nlgFactory.createCoordinatedPhrase();
	    c.addCoordinate(pp);
	    c.addCoordinate(sp1);	
	    c.addComplement(sp2);
		return nlgFactory.createSentence(c);
	}
	public static DocumentElement sentence6() {
		SPhraseSpec sp = nlgFactory.createClause();
		
		NPPhraseSpec np= nlgFactory.createNounPhrase(); 
		NPPhraseSpec np1= nlgFactory.createNounPhrase(); 

		PPPhraseSpec pp = nlgFactory.createPrepositionPhrase();
		
		VPPhraseSpec vp = nlgFactory.createVerbPhrase(); 
		VPPhraseSpec vp1 = nlgFactory.createVerbPhrase(); 

		sp.setVerbPhrase(vp);
		sp.setSubject(np);
		np.setSpecifier("the");
		np.setNoun("building");
		vp.setVerb("offer");
		vp.setObject(getPCell("Amenities"));
		
		
		pp.setPreposition("as");
		pp.setObject("amenities");
		sp.addComplement(pp);
		
		sp.setFeature(Feature.TENSE, Tense.PRESENT);
		return nlgFactory.createSentence(sp);
	}
	public static DocumentElement sentence7() {
		SPhraseSpec sp = nlgFactory.createClause();
		
		NPPhraseSpec np = nlgFactory.createNounPhrase(); 
		NPPhraseSpec np1 = nlgFactory.createNounPhrase(); 

		PPPhraseSpec pp = nlgFactory.createPrepositionPhrase();
		
		VPPhraseSpec vp= nlgFactory.createVerbPhrase(); 
		
		
		sp.setVerbPhrase(vp);
		vp.setVerb("build");
		vp.setObject(getPCell("Bldg Name"));

		vp.setFeature(Feature.PASSIVE, true);

		
		pp.setPreposition("in");
		pp.setObject(getPCell("Build Year"));
		//np1.setNoun("2000");
		sp.addPostModifier(pp);
		return nlgFactory.createSentence(sp);
	}
	public static DocumentElement sentence8() {
		SPhraseSpec sp = nlgFactory.createClause();
		SPhraseSpec sp1 = nlgFactory.createClause();

		NPPhraseSpec np = nlgFactory.createNounPhrase(); 
		NPPhraseSpec np1 = nlgFactory.createNounPhrase(); 

		PPPhraseSpec pp1 = nlgFactory.createPrepositionPhrase();
		PPPhraseSpec pp2 = nlgFactory.createPrepositionPhrase();

		VPPhraseSpec vp1= nlgFactory.createVerbPhrase(); 
		
		sp.setObject(np);
		np.setNoun("owner");
		np.setPreModifier("primary");
		np.setSpecifier("the");
		np.addComplement(pp1);
		pp1.setPreposition("of");
		pp1.setComplement(np1);
		np1.setNoun(getPCell("Bldg Name"));
		sp.setVerb("is");
		sp.setSubject(getPCell("Primary Owner"));
		
	
		return nlgFactory.createSentence(sp);
	}

	public static DocumentElement sentence9() {
		SPhraseSpec sp = nlgFactory.createClause();
		SPhraseSpec sp1 = nlgFactory.createClause();

		NPPhraseSpec np= nlgFactory.createNounPhrase(); 
		NPPhraseSpec np1= nlgFactory.createNounPhrase(); 

		
		PPPhraseSpec pp1 = nlgFactory.createPrepositionPhrase();
		PPPhraseSpec pp2 = nlgFactory.createPrepositionPhrase();

		VPPhraseSpec vp1= nlgFactory.createVerbPhrase(); 
		VPPhraseSpec vp2= nlgFactory.createVerbPhrase(); 

		sp.setVerb("is");
		sp.setSubject(np);
		np.setNoun("building");
		np.setSpecifier("the");
		sp.addComplement(vp1);
		vp1.setVerb("managed");
		vp1.setObject(pp1);
		vp1.setFeature(Feature.TENSE, Tense.PAST);
		pp1.setPreposition("by");
		
		pp1.setObject(getPCell("Management Company"));
		
		sp1.setVerb("is");
		sp1.addComplement(vp2);
		vp2.setVerb("lease");
		vp2.setObject(pp2);
		vp2.setFeature(Feature.TENSE, Tense.PAST);
		pp2.setPreposition("by");
		
		pp2.setObject(getPCell("Leasing Company"));
		
		//return nlgFactory.createSentence(sp);
		CoordinatedPhraseElement c = nlgFactory.createCoordinatedPhrase();
	    c.addCoordinate(sp);
	    c.addCoordinate(sp1);	
		return nlgFactory.createSentence(c);
	}
	public static DocumentElement sentence10() {
		SPhraseSpec sp = nlgFactory.createClause();
		
		NPPhraseSpec np = nlgFactory.createNounPhrase(); 
		NPPhraseSpec np1 = nlgFactory.createNounPhrase(); 
		NPPhraseSpec np2 = nlgFactory.createNounPhrase(); 

		PPPhraseSpec pp1 = nlgFactory.createPrepositionPhrase();
		
		VPPhraseSpec vp1= nlgFactory.createVerbPhrase(); 
		
		sp.setSubject(np);
		np.setNoun("It");
		sp.setVerbPhrase(vp1);
		vp1.setVerb("features");
		vp1.setObject(np1); 
		np1.setNoun("view");
		np1.setPreModifier("beautiful");
		np1.setSpecifier("a");
		np1.setComplement(pp1);
		pp1.setObject(np2);
		pp1.setPreposition("of");
		np2.setNoun(getPCell("View"));
		np2.setSpecifier("the");
		return nlgFactory.createSentence(sp);
	}
	public static DocumentElement sentence11() {
		SPhraseSpec sp = nlgFactory.createClause();
		SPhraseSpec sp1 = nlgFactory.createClause();

		NPPhraseSpec np = nlgFactory.createNounPhrase(); 
		NPPhraseSpec np1 = nlgFactory.createNounPhrase(); 
		NPPhraseSpec np2 = nlgFactory.createNounPhrase(); 

		PPPhraseSpec pp1 = nlgFactory.createPrepositionPhrase();
		
		VPPhraseSpec vp1= nlgFactory.createVerbPhrase(); 
		sp.setSubject(rests[0]);
		sp.setVerb("is");
		sp.setObject(np);
		
		np.setNoun("restaurant");
		np.setPreModifier(rests[1] + " star");
		np.setSpecifier("a");
		np.addComplement(np1);
		np1.setNoun("miles");
		np1.addPreModifier(rests[2]);
	    np1.setFeature(Feature.NUMBER, NumberAgreement.PLURAL);

		np1.addPostModifier("away");
		
		sp1.setVerbPhrase(vp1); 
		vp1.setObject(np2);
		np2.setPreModifier(rests[3]);
		np2.setNoun("walk");
		
		
		CoordinatedPhraseElement c = nlgFactory.createCoordinatedPhrase();
	    c.addCoordinate(sp);
	    c.addCoordinate(sp1);	
		return nlgFactory.createSentence(c);
	}
	public static DocumentElement sentence12() {
		SPhraseSpec sp = nlgFactory.createClause();
		SPhraseSpec sp1 = nlgFactory.createClause();

		NPPhraseSpec np = nlgFactory.createNounPhrase(); 
		NPPhraseSpec np1 = nlgFactory.createNounPhrase(); 
		NPPhraseSpec np2 = nlgFactory.createNounPhrase(); 

		PPPhraseSpec pp1 = nlgFactory.createPrepositionPhrase();
		
		VPPhraseSpec vp1= nlgFactory.createVerbPhrase(); 
		sp.setSubject(airport[0]);
		sp.setVerb("is");
		sp.setObject(np);
		
		np.setNoun(airport[2]);
		np.setSpecifier("a");
		np.addPostModifier("drive from this location");

		return nlgFactory.createSentence(sp);
	}
	
	
}
