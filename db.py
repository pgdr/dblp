#!/usr/bin/env python3
import re

import argparse
import json
from pathlib import Path
from typing import Optional
import gzip
import pprint
from lxml import etree


def normalize(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


CONFERENCES = {
    "IJCNN": "International Joint Conference on Neural Networks",
    "CSR": "Computer Science Symposium in Russia",
    "APPROX": "Approximation Algorithms for Combinatorial Optimization Problems",
    "RANDOM": "Randomization and Computation",
    "ITCS": "Innovations in Theoretical Computer Science",
    "LATIN": "Latin American Theoretical Informatics Symposium",
    "EMISA": "Entwicklungsmethoden fur Informationssysteme und deren Anwendung",
    "SecCo": "Security Issues in Coordination Models, Languages, and Systems",
    "SECCO": "Security Issues in Coordination Models, Languages, and Systems",
    "TriCoLore": "TriCoLore (C3GI/ISD/SCORE)",
    "TERMGRAPH": "Computing with Terms and Graphs",
    "EXPRESS": "Expressiveness in Concurrency",
    "SERA": "Software Engineering Research, Management and Applications",
    "SYNT": "Workshop on Synthesis",
    "LFMTP": "Logical Frameworks and Meta-languages: Theory and Practice",
    "AMMSE": "Algebraic Methods in Model-based Software Engineering",
    "TiCSA": "Trends in Configurable Systems Analysis",
    "ThEdu": "Theorem proving components for Educational software",
    "WoC": "Workshop on Continuations",
    "WWV": "Automated Specification and Verification of Web Systems",
    "SOS": "Structural Operational Semantics",
    "SOFSEM": "Current Trends in Theory and Practice of Informatics",
    "SCAV": "Safe Control of Autonomous Vehicles",
    "REFINE": "International Refinement Workshop",
    "DCM": "Developments in Computational Models",
    "FESCA": "Formal Engineering Approaches to Software Components and Architectures",
    "QPL": "Quantum Physics and Logic",
    "ICE": "Interaction and Concurrency Experience",
    "GANDALF": "Games, Automata, Logics, and Formal Verification",
    "QAPL": "Quantitative Aspects of Programming Languages and Systems",
    "GCM": "Graph Computation Models",
    "FICS": "Fixed Points in Computer Science",
    "BEAT": "Behavioural Types",
    "LSFA": "Logical and Semantic Frameworks, with Applications",
    "FOCLASA": "Foundations of Coordination Languages and Software Architectures",
    "HCVS": "Horn Clauses for Verification and Synthesis",
    "PLACES": "Programming Language Approaches to Concurrency and Communication",
    "WG": "Graph-Theoretic Concepts in Computer Science",
    "MFCS": "Mathematical Foundations of Computer Science",
    "FSTTCS": "Foundations of Software Technology and Theoretical Computer Science",
    "ALENEX": "Symposium on Algorithm Engineering and Experiments",
    "CCC": "Computational Complexity Conference",
    "FCT": "International Symposium on Fundamentals of Computation Theory",
    "FOCS": "IEEE Symposium on Foundations of Computer Science",
    "ICALP": "International Colloquium on Automata, Languages and Programming",
    "ISAAC": "International Symposium on Algorithms and Computation",
    "STACS": "Symposium on Theoretical Aspects of Computer Science",
    "STOC": "Symposium on Theory of Computing",
    "ESA": "European Symposium on Algorithms",
    "IPEC": "International Symposium on Parameterized and Exact Computation",
    "SODA": "Symposium on Discrete Algorithms",
    "SWAT": "Scandinavian Symposium and Workshops on Algorithm Theory",
    "WADS ": "Algorithms and Data Structures Symposium",
    "GD": "International Symposium on Graph Drawing",
    "SoCG": "Symposium on Computational Geometry",
    "CIAA": "International Conference on Implementation and Application of Automata",
    "CCC": "Computational Complexity Conference",
    "DCFS": "International Workshop on Descriptional Complexity of Formal Systems",
    "DLT": "International Conference on Developments in Language Theory",
    "ISSAC": "International Symposium on Symbolic and Algebraic Computation",
    "Petri Nets": "International Conference on Applications and Theory of Petri Nets and Concurrency",
    "RP": "International Conference on Reachability Problems",
    "SEA": "Symposium on Experimental Algorithms",
    "CC": "International Conference on Compiler Construction",
    "ESOP": "ETAPS European Symposium on Programming",
    "HOPL": "SIGPLAN History of Programming Languages Conference",
    "ICFP": "SIGPLAN International Conference on Functional Programming",
    "ICLP": "ALP International Conference on Logic Programming",
    "OOPSLA": "SIGPLAN Conference on Object:Oriented Programming, Systems, Languages, and Applications",
    "POPL": "SIGPLAN:SIGACT Symposium on Principles of Programming Languages",
    "PLDI": "SIGPLAN Conference on Programming Language Design and Implementation",
    "ASE": "International Conference on Automated Software Engineering",
    "ICSE": "International Conference on Software Engineering",
    "ICSR": "International Conference on Software Reuse",
    "SKG": "Semantics, Knowledge and Grid",
    "VMBO": "Value Modeling and Business Ontologies",
    "ISSRE": "International Symposium on Software Reliability Engineering",
    "FoSSaCS": "ETAPS International Conference on Foundations of Software Science and Computation Structures",
    "FASE": "ETAPS International Conference on Fundamental Approaches to Software Engineering",
    "WWDC": "Worldwide Developers Conference",
    "CAV": "Computer Aided Verification",
    "FORTE": "IFIP International Conference on Formal Techniques for Networked and Distributed Systems",
    "IJCAR": "International Joint Conference on Automated Reasoning",
    "LICS": "Symposium on Logic in Computer Science",
    "LPAR": "International Conference on Logic for Programming, Artificial Intelligence and Reasoning",
    "TACAS": "ETAPS International Conference on Tools and Algorithms for the Construction and Analysis of Systems",
    "RuleML": "RuleML Symposium",
    "WoLLIC": "Workshop on Logic, Language, Information and Computation",
    "CONCUR": "International Conference on Concurrency Theory",
    "DISC": "International Symposium on Distributed Computing",
    "DSN": "International Conference on Dependable Systems and Networks",
    "ICDCS": "International Conference on Distributed Computing Systems",
    "IPDPS": "International Parallel and Distributed Processing Symposium",
    "PODC": "Symposium on Principles of Distributed Computing",
    "SIROCCO": "International Colloquium on Structural Information and Communication Complexity",
    "SPAA": "Symposium on Parallelism in Algorithms and Architectures",
    "SRDS": "International Symposium on Reliable Distributed Systems",
    "HiPC": "International Conference on High Performance Computing",
    "SC": "International Conference for High Performance Computing, Networking, Storage, and Analysis",
    "ATC": "USENIX Annual Technical Conference",
    "SOSP": "Symposium on Operating Systems Principles",
    "OSDI": "USENIX Symposium on Operating Systems Design and Implementation",
    "ASPLOS": "International Conference on Architectural Support for Programming Languages and Operating Systems",
    "ISSCC": "International Solid:State Circuits Conference",
    "ISCA": "International Symposium on Computer Architecture",
    "MICRO": "International Symposium on Microarchitecture",
    "ASP:DAC": "Asia and South Pacific Design Automation Conference",
    "DAC": "Design Automation Conference",
    "DATE": "Design, Automation, and Test in Europe",
    "ICCAD": "International Conference on Computer:Aided Design",
    "ISPD": "International Symposium on Physical Design",
    "NSDI": "USENIX Symposium on Networked Systems Design and Implementation",
    "GlobeCom": "Global Communications Conference",
    "ICC": "International Conference on Communications",
    "ICSOC": "International Conference on Service Oriented Computing",
    "SIGMETRICS": "SIGMETRICS",
    "WINE": "The Workshop on Internet & Network Economics",
    "EWSN": "European Conference on Wireless Sensor Networks",
    "ISWC": "International Symposium on Wearable Computers",
    "CCS": "Computer and Communications Security",
    "DSN": "International Conference on Dependable Systems and Networks",
    "NDSS": "Network and Distributed System Security",
    "S&P": "Symposium on Security and Privacy",
    "USENIX Security": "USENIX Security Symposium",
    "ANTS": "Algorithmic Number Theory Symposium",
    "RSA": "RSA Conference",
    "BTW": "GI Conference on Database Systems for Business, Technology and Web",
    "ECIR": "European Conference on Information Retrieval",
    "ECIS": "European Conference on Information Systems",
    "ER": "International Conference on Conceptual Modeling",
    "ICDT": "International Conference on Database Theory",
    "ICIS": "International Conference on Information Systems",
    "ISWC": "International Semantic Web Conference",
    "JCDL": "Joint Conference on Digital Libraries",
    "PODS": "Symposium on Principles of Database Systems",
    "SIGMOD": "Special Interest Group on Management of Data",
    "WWW": "World Wide Web Conference",
    "AAAI": "AAAI Conference on Artificial Intelligence",
    "PT-AI": "Philosophy and Theory of Artificial Intelligence",
    "EGC": "Extraction et Gestion des connaissances",
    "KDM": "Knowledge Discovery and Management",
    "FLAIRS": "Florida Artificial Intelligence Research Society Conference",
    "AAMAS": "International Conference on Autonomous Agents and Multiagent Systems",
    "ICAPS": "International Conference on Automated Planning and Scheduling",
    "CIBB": "International Conference on Computational Intelligence Methods for Bioinformatics and Biostatistics",
    "AREA": "Agents and Robots for reliable Engineered Autonomy",
    "ECAI": "European Conference on Artificial Intelligence",
    "ECML PKDD": "European Conference on Machine Learning and Principles and Practice of Knowledge Discovery in Databases",
    "ICML": "International Conference on Machine Learning",
    "ICLR": "International Conference on Learning Representations",
    "IJCAI": "International Joint Conference on Artificial Intelligence",
    "ISWC": "International Semantic Web Conference",
    "NeurIPS": "Conference on Neural Information Processing Systems",
    "CEC": "Congress on Evolutionary Computation",
    "EvoStar": "EvoStar Conference",
    "FOGA": "Foundations of Genetic Algorithms",
    "GECCO": "Genetic and Evolutionary Computation Conference",
    "PPSN": "Parallel Problem Solving from Nature",
    "CVPR": "Conference on Computer Vision and Pattern Recognition",
    "ECCV": "European Conference on Computer Vision",
    "ICCV": "International Conference on Computer Vision",
    "SCIA": "Scandinavian Conference on Image Analysis",
    "EMNLP": "Empirical Methods in Natural Language Processing",
    "COLING": "International Committee on Computational Linguistics",
    "TSD": "Text, Speech and Dialogue",
    "CICLing": "International Conference on Intelligent Text Processing and Computational Linguistics",
    "MMB": "Messung, Modellierung und Bewertung",
    "MM": "International Conference on Multimedia",
    "SGP": "Symposium on Geometry Processing",
    "SIGGRAPH": "International Conference on Computer Graphics and Interactive Techniques",
    "CHI": "Conference on Human Factors in Computing Systems",
    "GI": "Graphics Interface",
    "MobileHCI": "Conference on Human-Computer Interaction with Mobile Devices and Services",
    "UIST": "Symposium on User Interface Software and Technology",
    "UMAP": "International Conference on User Modeling, Adaptation, and Personalization",
    "CIBB": "International Conference on Computational Intelligence Methods for Bioinformatics and Biostatistics",
    "ISMB": "Intelligent Systems for Molecular Biology",
    "PSB": "Pacific Symposium on Biocomputing",
    "RECOMB": "Research in Computational Molecular Biology",
    "ACL": "Association for Computational Linguistics",
    "ICSEM": "Smart Engineering Materials",
    "COORDINATION": "Coordination Models and Languages",
    "EUROCOMB": "European Conference on Combinatorics, Graph Theory and Applications",
    "DL": "Description Logics",
    "ICIAAAAI": "Interaction Challenges for Intelligent Assistants",
    "KR": "Principles of Knowledge Representation and Reasoning",
    "SOCS": "Symposium on Combinatorial Search",
    "STAIRS": "European Starting AI Researchers Symposium",
    "AIES": "Conference on AI, Ethics, and Society",
    "MRC": "Workshop on Machine Reasoning",
    "CoRR": "arXiv",
}

JOURNALS = {
    "ACMCR": "ACM Computing Reviews",
    "CSUR": "ACM Computing Surveys",
    "TALG": "ACM Transactions on Algorithms",
    "TOCL": "ACM Transactions on Computational Logic",
    "TODS": "ACM Transactions on Database Systems",
    "TOG": "ACM Transactions on Graphics",
    "TOIS": "ACM Transactions on Information Systems",
    "TOMM": "ACM Transactions on Multimedia Computing, Communications, and Applications",
    "TOPLAS": "ACM Transactions on Programming Languages and Systems",
    "TOSEM": "ACM Transactions on Software Engineering and Methodology",
    "ActaInf": "Acta Informatica",
    "AB": "Adaptive Behavior",
    "ALGOLBull": "ALGOL Bulletin",
    "Algorithmica": "Algorithmica",
    "Algorithms": "Algorithms",
    "AAI": "Applied Artificial Intelligence",
    "ACME": "Archives of Computational Methods in Engineering",
    "AIJ": "Artificial Intelligence",
    "AstroComp": "Astronomy and Computing",
    "AAMAS": "Autonomous Agents and Multi-Agent Systems",
    "JBCS": "Journal of the Brazilian Computer Society",
    "ClusterComput": "Cluster Computing",
    "CodeWords": "Code Words",
    "CSR": "Cognitive Systems Research",
    "Combinatorica": "Combinatorica",
    "CPC": "Combinatorics, Probability and Computing",
    "CACM": "Communications of the ACM",
    "CyS": "Computación y Sistemas",
    "CMOT": "Computational and Mathematical Organization Theory",
    "CI": "Computational Intelligence",
    "ComputMech": "Computational Mechanics",
    "CAS": "Computer Aided Surgery",
    "CJ": "The Computer Journal",
    "CLSR": "Computer Law & Security Review",
    "CompNet": "Computer Networks",
    "COAP": "Computational Optimization and Applications",
    "CompSci": "Computer Science",
    "CAG": "Computers & Graphics",
    "Computing": "Computing",
    "CHK": "Cybernetics and Human Knowing",
    "DKE": "Data & Knowledge Engineering",
    "DMKD": "Data Mining and Knowledge Discovery",
    "DTA": "Data Technologies and Applications",
    "DMTCS": "Discrete Mathematics & Theoretical Computer Science",
    "DistribComput": "Distributed Computing",
    "EISEJ": "e-Informatica Software Engineering Journal",
    "ELCVIA": "Electronic Letters on Computer Vision and Image Analysis",
    "ENTCS": "Electronic Notes in Theoretical Computer Science",
    "EPTCS": "Electronic Proceedings in Theoretical Computer Science",
    "EMSE": "Empirical Software Engineering",
    "EURASIPJASP": "EURASIP Journal on Advances in Signal Processing",
    "EC": "Evolutionary Computation",
    "FirstMonday": "First Monday",
    "FAC": "Formal Aspects of Computing",
    "FnTCommIT": "Foundations and Trends in Communications and Information Theory",
    "FnTCGV": "Foundations and Trends in Computer Graphics and Vision",
    "FnTTCS": "Foundations and Trends in Theoretical Computer Science",
    "FI": "Fundamenta Informaticae",
    "FGCS": "Future Generation Computer Systems",
    "FSS": "Fuzzy Sets and Systems",
    "HOSC": "Higher-Order and Symbolic Computation",
    "Hipertext": "Hipertext.net",
    "ICGAJ": "ICGA Journal",
    "ICTExpress": "ICT Express",
    "TON": "IEEE/ACM Transactions on Networking",
    "IEEEAnnHistComp": "IEEE Annals of the History of Computing",
    "IEEEIntellSyst": "IEEE Intelligent Systems",
    "IEEEInternetComput": "IEEE Internet Computing",
    "IEEEMicro": "IEEE Micro",
    "IEEEMM": "IEEE MultiMedia",
    "IEEESoftware": "IEEE Software",
    "TC": "IEEE Transactions on Computers",
    "TCST": "IEEE Transactions on Control Systems Technology",
    "TDSC": "IEEE Transactions on Dependable and Secure Computing",
    "TEC": "IEEE Transactions on Evolutionary Computation",
    "TFS": "IEEE Transactions on Fuzzy Systems",
    "TIFS": "IEEE Transactions on Information Forensics and Security",
    "TIT": "IEEE Transactions on Information Theory",
    "TLT": "IEEE Transactions on Learning Technologies",
    "TMC": "IEEE Transactions on Mobile Computing",
    "TMM": "IEEE Transactions on Multimedia",
    "TNNLS": "IEEE Transactions on Neural Networks and Learning Systems",
    "TPAMI": "IEEE Transactions on Pattern Analysis and Machine Intelligence",
    "TSE": "IEEE Transactions on Software Engineering",
    "TVCG": "IEEE Transactions on Visualization and Computer Graphics",
    "ISJ": "The Imaging Science Journal",
    "InfoComp": "Information and Computation",
    "IST": "Information and Software Technology",
    "IPL": "Information Processing Letters",
    "ISU": "Information Services & Use",
    "InfoSystems": "Information Systems",
    "InfoSystemsJ": "Information Systems Journal",
    "ISSE": "Innovations in Systems and Software Engineering",
    "IIASSRC": "International Institute for Advanced Studies in Systems Research and Cybernetics",
    "IJACT": "International Journal of Advanced Computer Technology",
    "IJAMCS": "International Journal of Applied Mathematics and Computer Science",
    "IJCGA": "International Journal of Computational Geometry and Applications",
    "IJCIA": "International Journal of Computational Intelligence and Applications",
    "IJCM": "International Journal of Computational Methods",
    "IJCARS": "International Journal of Computer Assisted Radiology and Surgery",
    "IJCPL": "International Journal of Computer Processing of Languages",
    "IJCV": "International Journal of Computer Vision",
    "IJCIS": "International Journal of Cooperative Information Systems",
    "IJCreativeComput": "International Journal of Creative Computing",
    "IJDWM": "International Journal of Data Warehousing and Mining",
    "IJeC": "International Journal of e-Collaboration",
    "IJFCS": "International Journal of Foundations of Computer Science",
    "IJHPCA": "International Journal of High Performance Computing Applications",
    "IJIG": "International Journal of Image and Graphics",
    "IJIA": "International Journal of Information Acquisition",
    "IJITDM": "International Journal of Information Technology & Decision Making",
    "IJITM": "International Journal of Innovation and Technology Management",
    "IJIIT": "International Journal of Intelligent Information Technologies",
    "IJMCS": "International Journal of Mathematics and Computer Science",
    "IJMBL": "International Journal of Mobile and Blended Learning",
    "IJMS": "International Journal of Modelling and Simulation",
    "IJPRAI": "International Journal of Pattern Recognition and Artificial Intelligence",
    "IJSM": "International Journal of Shape Modeling",
    "IJSI": "International Journal of Software and Informatics",
    "IJSEKE": "International Journal of Software Engineering and Knowledge Engineering",
    "IJUFKS": "International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems",
    "IJWMIP": "International Journal of Wavelets, Multiresolution and Information Processing",
    "IJWSR": "International Journal of Web Services Research",
    "IJWIN": "International Journal of Wireless Information Networks",
    "IJAIT": "International Journal on Artificial Intelligence Tools",
    "IJSWIS": "International Journal on Semantic Web and Information Systems",
    "InternetHistories": "Internet Histories",
    "JAIF": "Journal of Advances in Information Fusion",
    "JAIR": "Journal of Artificial Intelligence Research",
    "JALC": "Journal of Automata, Languages and Combinatorics",
    "JAR": "Journal of Automated Reasoning",
    "JBCB": "Journal of Bioinformatics and Computational Biology",
    "JCasesIT": "Journal of Cases on Information Technology",
    "JCIM": "Journal of Chemical Information and Modeling",
    "JCheminf": "Journal of Cheminformatics",
    "JCSCircuits": "Journal of Circuits, Systems, and Computers",
    "JCN": "Journal of Communications and Networks",
    "JCG": "Journal of Computational Geometry",
    "JCSS": "Journal of Computer and System Sciences",
    "JCMC": "Journal of Computer-Mediated Communication",
    "JCSC": "Journal of Computing Sciences in Colleges",
    "JCryptol": "Journal of Cryptology",
    "JDM": "Journal of Database Management",
    "JETAI": "Journal of Experimental and Theoretical Artificial Intelligence",
    "JFR": "Journal of Formalized Reasoning",
    "JFP": "Journal of Functional Programming",
    "JGIM": "Journal of Global Information Management",
    "JGAA": "Journal of Graph Algorithms and Applications",
    "JGT": "Journal of Graphics Tools",
    "JGridComput": "Journal of Grid Computing",
    "JITP": "Journal of Information Technology & Politics",
    "JIntellRobotSyst": "Journal of Intelligent and Robotic Systems",
    "JIN": "Journal of Interconnection Networks",
    "JLC": "Journal of Logic and Computation",
    "JLLI": "Journal of Logic, Language and Information",
    "JLAMP": "Journal of Logical and Algebraic Methods in Programming",
    "JMLR": "Journal of Machine Learning Research",
    "JMultimedia": "Journal of Multimedia",
    "JOT": "The Journal of Object Technology",
    "JOEUC": "Journal of Organizational and End User Computing",
    "JSEP": "Journal of Software: Evolution and Process",
    "JStatSoft": "Journal of Statistical Software",
    "JSIS": "Journal of Strategic Information Systems",
    "JSupercomput": "The Journal of Supercomputing",
    "JSC": "Journal of Symbolic Computation",
    "JSystemsSoftware": "Journal of Systems and Software",
    "JACM": "Journal of the ACM",
    "JWS": "Journal of Web Semantics",
    "Kybernetes": "Kybernetes",
    "LMCS": "Logical Methods in Computer Science",
    "ML": "Machine Learning",
    "MVA": "Machine Vision and Applications",
    "MCE": "Mathematics and Computer Education",
    "MindsMachines": "Minds and Machines",
    "MCCR": "Mobile Computing and Communications Review",
    "MolInf": "Molecular Informatics",
    "NatComput": "Natural Computing",
    "NeuralNetw": "Neural Networks",
    "Neurocomputing": "Neurocomputing",
    "PPL": "Parallel Processing Letters",
    "PRL": "Pattern Recognition Letters",
    "PeerJCS": "PeerJ Computer Science",
    "PerfEval": "Performance Evaluation",
    "PUC": "Personal and Ubiquitous Computing",
    "Presence": "Presence: Teleoperators & Virtual Environments",
    "PEIS": "Probability in the Engineering and Informational Sciences",
    "ProcIEEE": "Proceedings of the IEEE",
    "ProgramELIS": "Program: Electronic Library and Information Systems",
    "ReCALL": "ReCALL",
    "ReScienceC": "ReScience C",
    "RLC": "Research on Language and Computation",
    "SSQ": "Science Software Quarterly",
    "SCI": "Scientific Computing & Instrumentation",
    "SICOMP": "SIAM Journal on Computing",
    "SISC": "SIAM Journal on Scientific Computing",
    "SimulGaming": "Simulation & Gaming",
    "SoSyM": "Software and Systems Modeling",
    "STVR": "Software Testing, Verification & Reliability",
    "TCS": "Theoretical Computer Science",
    "TIES": "Theoretical Issues in Ergonomics Science",
    "TAOSD": "Transactions on Aspect Oriented Software Development",
    "TGDK": "Transactions on Graph Data and Knowledge",
    "TUGboat": "TUGboat",
    # Correct below
    "JCSS": "Journal of Computer and System Sciences",
    "TALG": "ACM Transactions on Algorithms",
    "TOCT": "ACM Transactions on Computation Theory",
    "Algorithmica": "Algorithmica",
    "SICOMP": "SIAM Journal on Computing",
    "COSREV": "Computer Science Review",
    "SIGKDD": "Conference on Knowledge Discovery and Data Mining",
    "KDD": "Knowledge Discovery and Data Mining",
    "ICSE": "Conference on Software Engineering",
    "JELIA": "European Conference on Logics in Artificial Intelligence",
    "CoRR": "arXiv",
}


for k, v in list(CONFERENCES.items()):
    CONFERENCES[k] = normalize(v)


def text_of(elem: Optional[etree._Element]) -> Optional[str]:
    if elem is None:
        return None
    text = " ".join("".join(elem.itertext()).split())
    return text or None


def first_child_text(
    elem: etree._Element, name: str
) -> Optional[str]:
    child = elem.find(name)
    return text_of(child)


def all_child_texts(elem: etree._Element, name: str) -> list[str]:
    values = []
    for child in elem.findall(name):
        value = text_of(child)
        if value:
            values.append(value)
    return values


def venue_of(elem: etree._Element) -> Optional[str]:
    return (
        first_child_text(elem, "journal")
        or first_child_text(elem, "booktitle")
        or ""
    )


def authors_of(elem: etree._Element) -> str:
    authors = all_child_texts(elem, "author")
    if authors:
        return "; ".join(authors)

    editors = all_child_texts(elem, "editor")
    return "; ".join(editors)


def slugify_conference(venue):
    nv = None
    for short, long in CONFERENCES.items():
        if short in venue:
            return short
        if nv is None:
            nv = normalize(venue)
        if long in nv:
            return short
    return nv


def slugify_journal(venue):
    nv = None
    for short, long in JOURNALS.items():
        if short in venue:
            return short
        if nv is None:
            nv = normalize(venue)
        if long in nv:
            return short
    return nv


SEEN = {}


from collections import defaultdict

TITLES = defaultdict(list)

FORBIDDEN = [
    "proceedings",
    "conference",
    "symposium",
    "editorial",
    "workshop",
    "bookreview",
    "erratum",
    "introduction",
    "preface",
    "frontmatter",
    "foreword",
]


def handle_record(elem, context):
    parent = elem.getparent()
    if parent is None or etree.QName(parent).localname != "dblp":
        return
    type_ = str(etree.QName(elem).localname).lower().strip()
    if type_ not in ["inproceedings", "article"]:
        return
    title = first_child_text(elem, "title")
    norm_title = normalize(title)
    for f in FORBIDDEN:
        if f in norm_title:
            return
    venue = venue_of(elem).strip()
    if type_ == "inproceedings":
        retval = slugify_conference(venue)
        SEEN[venue] = retval
        venue = retval
    if type_ == "journal":
        retval = slugify_journal(venue)
        venue = retval
    if venue == "CoRR":
        return
    year = first_child_text(elem, "year")
    if year is None:
        year = 1824
    try:
        year = int(year)
    except:
        ...
    H = hash(norm_title)
    item = {
        "type": type_,
        "author": authors_of(elem),
        "title": title,
        "venue": venue,
        "hash": H,
        "year": year,
    }
    # TITLES[H].append(item)
    # if len(TITLES) > 1000*1000:
    #    exit("HOLY TOLEDO")

    elem.clear()
    while elem.getprevious() is not None:
        del parent[0]
    return item


def iter_dblp_records(xml_path: str):
    xml_path = Path(xml_path)

    opener = gzip.open if xml_path.suffix == ".gz" else open
    with opener(xml_path, "rb") as f:
        context = etree.iterparse(
            f,
            events=("end",),
            load_dtd=True,
            huge_tree=True,
            recover=True,
        )

        for _, elem in context:
            retval = handle_record(elem, context)
            if retval:
                yield retval


def write_json_array(records, output_path: str) -> int:
    count = 0
    first = True

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("[\n")
        for rec in records:
            if not rec["venue"]:
                continue
            if not first:
                f.write(",\n")
            json.dump(rec, f, ensure_ascii=False)
            first = False
            count += 1
        f.write("\n]\n")

    return count


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Extract DBLP records to JSON: type, author, title, venue."
    )
    ap.add_argument("xml", help="Path to dblp.xml")
    ap.add_argument(
        "-o",
        "--output",
        default="dblp_items.json",
        help="Output JSON file (default: dblp_items.json)",
    )
    args = ap.parse_args()

    count = write_json_array(
        iter_dblp_records(args.xml),
        args.output,
    )

    print(f"Wrote {count} records to {args.output}")


if __name__ == "__main__":
    main()
