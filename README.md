GAAF : Genome Assembly Analysis Framework

GAAF is an analysis framework, in the context of Genome Assembly domain, which aims to facilitate the process of post analysis. It emerged from the issue related to the quality interpretation of assembled genome data.
GAAF architecture is divided into three main modules: Reads Generator, Genome Assembly and Assembly Evaluation.
 
Reads Generator: as the name mentions, this Module is responsible for generating artificial reads. The way it is done depends on the chosen algorithm, e.g. pIRS (Hu et al. 2012) or Grinder (Angly et al. 2012)- in Escalona article (Escalona et al. 2016 many options are listed. The Module may receive or not a genome reference entry. When no input is available, the reads are randomly generated, according to each algorithm. In addition, it could also receive raw reads, in order to filter them in a quality trimming hot spot, or by modifying them in any purposes. 
Genome Assembly: this is the module where the reads are assembled. It may output contigs, or scaffolds, which may be analyzed on Assembly Evaluation Module, or may work as re-input to Genome Assembly, calling hot spots capable of scaffolding, gap filling etc. It works with distinct assemblers, file formats and sequencing technologies.
Assembly Evaluation: the metrics or features qualifying the assemblies are generated in the Assembly Evaluation Module. Not only the evaluation metrics, but also some other post-analysis could be included here, such as genome comparisons. Those results, according to each application, may be still analyzed in external modules, like in a Statistics Module.

INSTALLATION:
You do not need to install the framework, in order to use its code. But, you do need to provide its dependencies :
python >=2.7
r
Perl >= 5.6
zlib and boost
biopython
scipy 
pandas  
However, we instantiate the framework in a study case, where you can see how it works, and how to install and use third-party tools.

Extensibility:
The greatest advantage about using a framework is the easy way of how a new item is added. For example, given the architecture figure, image any red box could be remove, and any new red box may be added. In Genome Assembly, we can freely add new assemblers, and then have all the old assemblies plus the new ones.
We now describe how to add new classes to each module.
Reads Generator
We provide pIRS code as example. Create you code keeping the__init__ and command methods, as in pIRS. 
__init__(self, exp,out)
command(self,sample)
The two most important things are the attributes.’ Files’ stores a list of the samples names. It does not include file formats. And 

