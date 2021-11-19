from math import sin, cos, pi, log10
from sys import float_info

from numpy import fft, convolve, linspace, array, vstack, lcm
import matplotlib.pyplot as plt

# f_s = 128 kHz, f_pa = 2 kHz, f_st = 2.56 kHz, gain_pa = 1 dB, ripple_pa = 0.28 dB, att_st = -98.48 dB, n_taps = 832
filter = [0.000007843720623236043, 0.000004278345295781511, 0.000005403667066221734, 0.000006691315452907781, 0.000008150045704110886, 0.00000978725611094941, 0.000011608996984880698, 0.000013619504364333407, 0.000015821201495131063, 0.000018214288011421873, 0.000020796570670036558, 0.000023563179035309233, 0.000026506378791440255, 0.000029615423861973183, 0.00003287635226432179, 0.00003627190886201023, 0.000039781341263945824, 0.000043380204546549804, 0.00004704050335408969, 0.00005073068873056898, 0.00005441556426289718, 0.00005805642295254431, 0.0000616111910251882, 0.00006503452939612308, 0.00006827813445641724, 0.00007129106772373328, 0.00007402000644792147, 0.00007640968474357385, 0.00007840337111312984, 0.00007994329085570354, 0.00008097125445283343, 0.0000814292294889786, 0.00008125983301336947, 0.00008040712470181444, 0.00007881727036824129, 0.00007643924515196579, 0.00007322560593960072, 0.000069132993436809, 0.0000641230199308996, 0.00005816317471750027, 0.00005122720702465441, 0.00004329622912604799, 0.000034358773177863244, 0.00002441217206516509, 0.000013462253379241917, 0.0000015250260932436688, -0.000011374683335187771, -0.000025200639048718578, -0.000039907391843692994, -0.00005543781265924578, -0.00007172486047116929, -0.00008869100726664171, -0.00010624778005518417, -0.00012429715414545613, -0.00014273141907304482, -0.00016143346375442532, -0.00018027812546977655, -0.00019913243214872875, -0.00021785642907628847, -0.0002363048394462032, -0.00025432781616982985, -0.00027177184977021814, -0.000288481701508917, -0.00030430188679278307, -0.0003190776369817763, -0.00033265659742357157, -0.00034489087939824556, -0.0003556383621072125, -0.0003647639478719413, -0.00037214159801174867, -0.0003776561552191149, -0.00038120443727980227, -0.00038269672658097575, -0.0003820586817783959, -0.0003792324914686392, -0.0003741778985872164, -0.0003668736040544923, -0.00035731795482855553, -0.00034552957412866856, -0.00033154842010564274, -0.0003154355888326931, -0.0002972733235857977, -0.00027716574592453883, -0.00025523791714505067, -0.00023163531609170232, -0.00020652386291798106, -0.00018008768980098334, -0.0001525297202780986, -0.000124068295999576, -0.00009493693873815591, -0.00006538116402237262, -0.000035657434180248525, -0.0000060300637869522105, 0.000023230509204295882, 0.00005185089553914594, 0.0000795567793351373, 0.00010607589207618957, 0.0001311409039616243, 0.00015449231724590354, 0.00017588169703929268, 0.00019507450362164447, 0.00021185289411595253, 0.0002260184818303832, 0.00023739462261928077, 0.00024582879240017197, 0.0002511948137689462, 0.0002533948480685339, 0.0002523615359642444, 0.0002480598527099588, 0.00024048836740597296, 0.00022968003782829373, 0.0002157022795080577, 0.00019865656863507874, 0.0001786783299691074, 0.0001559370040308809, 0.00013063572285978273, 0.0001030103372114418, 0.00007332727057153378, 0.00004188007983490808, 0.000008986141052938425, -0.000025015420382794053, -0.0000597648435239552, -0.00009488375591619706, -0.00012998055684633713, -0.00016465832424012215, -0.00019851985490222583, -0.0002311660005961874, -0.00026219407114439766, -0.00029121116694135965, -0.0003178529521717158, -0.00034176866086093054, -0.00036259769180095337, -0.000380064037607924, -0.0003938684545478567, -0.00040377863032597667, -0.0004095865011481009, -0.00041112935422556683, -0.0004082874857247505, -0.0004009877671280609, -0.0003892052149924187, -0.0003729646779954726, -0.0003523416566253701, -0.00032746269947154865, -0.0002985051407756325, -0.00026569630476472707, -0.000229312273588053, -0.00018967580918116832, -0.0001471537836846092, -0.00010215425682824557, -0.00005512275851308814, -0.000006538129524184674, 0.00004309200179747732, 0.00009323633379971508, 0.00014334539734493274, 0.00019285729618983638, 0.00024120378709679795, 0.0002878165770709132, 0.0003321337258089977, 0.0003736062688506139, 0.00041170480010448157, 0.00044592580363879246, 0.00047579797516198916, 0.0005008883845701094, 0.0005208082939190553, 0.0005352187121164756, 0.0005438352706939971, 0.0005464327395366827, 0.0005428491632207548, 0.0005329890088078192, 0.0005168258169870346, 0.0004944041835739037, 0.00046584063660783586, 0.000431324450055965, 0.000391116555802778, 0.00034554887777392786, 0.00029502115182460564, 0.00023999966108502962, 0.00018101095571606833, 0.00011864041665267685, 0.00005352304340437133, -0.000013658831150507367, -0.00008218491603536522, -0.00015130374925648982, -0.0002202395317215665, -0.00028820198017881244, -0.0003543943076738356, -0.00041802158263819515, -0.00047830108691105684, -0.0005344710675331729, -0.0005857992578673142, -0.0006315928237496245, -0.0006712073306869049, -0.0007040544378735058, -0.0007296101342453403, -0.00074742277626912, -0.0007571194729701421, -0.0007584116112520549, -0.0007511005127290484, -0.0007350820695666818, -0.0007103495905249487, -0.0006769959128444833, -0.0006352149637547267, -0.000585301724233503, -0.0005276507775505978, -0.0004627540773883175, -0.00039119738433470065, -0.00031365558789641864, -0.00023088724840840297, -0.00014372740877295807, -0.0000530794135812432, 0.00004009330845272015, 0.00013477726342077335, 0.00022991990724017595, 0.0003244404697876014, 0.000417242110639473, 0.0005072240121419497, 0.0005932933417959479, 0.0006743792227901712, 0.0007494441437311685, 0.000817498097837222, 0.0008776096510962619, 0.0009289191850318768, 0.0009706493923198387, 0.0010021168270535825, 0.0010227407683432643, 0.001032052906747118, 0.001029704649474236, 0.001015474237183418, 0.000989272105808993, 0.0009511444883473427, 0.0009012758235801954, 0.00083998929562144, 0.0007677461820400234, 0.0006851439794862671, 0.0005929124336140955, 0.0004919079810065394, 0.00038310639941104474, 0.00026759372492077656, 0.00014655630811094485, 0.000021269732776830692, -0.00010691385041080575, -0.00023657966545821663, -0.0003662656228678478, -0.0004944786417629195, -0.0006197108731105526, -0.0007404558934504534, -0.000855225949970909, -0.0009625702506836625, -0.0010610931779006438, -0.0011494712830100603, -0.0012264687733368777, -0.0012909532205746962, -0.0013419124397293153, -0.001378469827779881, -0.0013998954747501482, -0.0014056157668337018, -0.001395225943125387, -0.0013685012143196942, -0.0013253984546678576, -0.0012660583148430655, -0.0011908163778121617, -0.0011002003122295141, -0.000994915790719297, -0.0008758672627872311, -0.0007441242595773033, -0.0006009342372185592, -0.0004476991452944222, -0.0002859689495020168, -0.0001174245121751005, 0.00005613781437073196, 0.0002328247974905868, 0.00041066572571757826, 0.0005876334577773431, 0.0007616662990892915, 0.0009306909211412733, 0.0010926459700895676, 0.0012455057874817628, 0.0013873044920201315, 0.0015161599108890337, 0.0016302968009115559, 0.0017280695480315516, 0.0018079839052070358, 0.0018687174372601382, 0.0019091385171741257, 0.0019283234769416758, 0.0019255717089461943, 0.001900418695963952, 0.0018526466567171573, 0.0017822924847919327, 0.001689653007641102, 0.0015752874926775115, 0.001440017221858243, 0.001284922104875704, 0.0011113341710461287, 0.0009208280531856993, 0.0007152087484632526, 0.0004964962605656626, 0.00026690748187752, 0.00002883562686647948, -0.00021517299351677294, -0.00046244421208314695, -0.0007102032874819869, -0.0009556043868967322, -0.0011957607970448994, -0.00142777710384698, -0.0016487810144776998, -0.001855957791523151, -0.0020465811515882654, -0.002218049686658729, -0.002367913967619183, -0.002493914246284927, -0.0025940043518061524, -0.002666383872029355, -0.002709523712027373, -0.002722187848903066, -0.002703456729536418, -0.0026527448413912564, -0.002569813925326349, -0.0024547857898612577, -0.0023081501781836438, -0.002130767092986931, -0.0019238668689271468, -0.0016890467728420057, -0.00142826192789647, -0.0011438119682003719, -0.0008383248520351903, -0.0005147366456420892, -0.00017626640213074752, 0.00017361239240286952, 0.0005312030436278312, 0.0008926203857346967, 0.001253828912738011, 0.0016106833001477091, 0.0019589709496246562, 0.0022944561632254777, 0.0026129255338193883, 0.0029102348224466015, 0.003182356339259055, 0.0034254254513039592, 0.003635786898701662, 0.003810040640840757, 0.00394508552694867, 0.004038161185861805, 0.004086887366754916, 0.004089299798255291, 0.004043883632724617, 0.00394960284300649, 0.0038059247522247578, 0.0036128412459395308, 0.0033708830823819392, 0.00308113167903406, 0.002745223343523324, 0.0023653502892283153, 0.001944253881882913, 0.0014852141071094419, 0.000992031341963065, 0.000469004779032836, -0.0000790961210529746, -0.0006470643260529116, -0.0012292935876614915, -0.001819821919322342, -0.0024123789091774987, -0.0030004373966169163, -0.0035772684345572875, -0.004135999107914709, -0.004669673743015509, -0.005171317068504762, -0.005633998683023302, -0.006050898496561322, -0.006415371973496939, -0.0067210152370760935, -0.006961730049573205, -0.007131786938321586, -0.007225885393415481, -0.007239211298619866, -0.007167491398440413, -0.007007044115924256, -0.006754825711433921, -0.00640847067735041, -0.005966326670648412, -0.005427484839469791, -0.004791803950737751, -0.00405992640436343, -0.0032332874431710576, -0.002314119547569132, -0.0013054496987460612, -0.00021108663047781848, 0.000964397917012124, 0.0022156912116477303, 0.0035367722718793325, 0.004920953507117078, 0.006360921252971188, 0.007848786378320281, 0.009376147078219417, 0.01093413923145777, 0.012513514161157662, 0.014104699334445636, 0.015697877907333832, 0.01728306167450295, 0.018850171219909843, 0.02038911489474462, 0.021889869925043152, 0.02334256282489775, 0.024737549580755185, 0.02606549401291689, 0.02731744418952969, 0.028484906230023734, 0.029559914255880965, 0.03053509631089723, 0.0314037356425885, 0.03215982656320307, 0.032798124686357094, 0.03331419078392762, 0.033704427878768456, 0.03396611146919811, 0.03409741245570781, 0.03409741245570781, 0.03396611146919811, 0.033704427878768456, 0.03331419078392762, 0.032798124686357094, 0.03215982656320307, 0.0314037356425885, 0.03053509631089723, 0.029559914255880965, 0.028484906230023734, 0.02731744418952969, 0.02606549401291689, 0.024737549580755185, 0.02334256282489775, 0.021889869925043152, 0.02038911489474462, 0.018850171219909843, 0.01728306167450295, 0.015697877907333832, 0.014104699334445636, 0.012513514161157662, 0.01093413923145777, 0.009376147078219417, 0.007848786378320281, 0.006360921252971188, 0.004920953507117078, 0.0035367722718793325, 0.0022156912116477303, 0.000964397917012124, -0.00021108663047781848, -0.0013054496987460612, -0.002314119547569132, -0.0032332874431710576, -0.00405992640436343, -0.004791803950737751, -0.005427484839469791, -0.005966326670648412, -0.00640847067735041, -0.006754825711433921, -0.007007044115924256, -0.007167491398440413, -0.007239211298619866, -0.007225885393415481, -0.007131786938321586, -0.006961730049573205, -0.0067210152370760935, -0.006415371973496939, -0.006050898496561322, -0.005633998683023302, -0.005171317068504762, -0.004669673743015509, -0.004135999107914709, -0.0035772684345572875, -0.0030004373966169163, -0.0024123789091774987, -0.001819821919322342, -0.0012292935876614915, -0.0006470643260529116, -0.0000790961210529746, 0.000469004779032836, 0.000992031341963065, 0.0014852141071094419, 0.001944253881882913, 0.0023653502892283153, 0.002745223343523324, 0.00308113167903406, 0.0033708830823819392, 0.0036128412459395308, 0.0038059247522247578, 0.00394960284300649, 0.004043883632724617, 0.004089299798255291, 0.004086887366754916, 0.004038161185861805, 0.00394508552694867, 0.003810040640840757, 0.003635786898701662, 0.0034254254513039592, 0.003182356339259055, 0.0029102348224466015, 0.0026129255338193883, 0.0022944561632254777, 0.0019589709496246562, 0.0016106833001477091, 0.001253828912738011, 0.0008926203857346967, 0.0005312030436278312, 0.00017361239240286952, -0.00017626640213074752, -0.0005147366456420892, -0.0008383248520351903, -0.0011438119682003719, -0.00142826192789647, -0.0016890467728420057, -0.0019238668689271468, -0.002130767092986931, -0.0023081501781836438, -0.0024547857898612577, -0.002569813925326349, -0.0026527448413912564, -0.002703456729536418, -0.002722187848903066, -0.002709523712027373, -0.002666383872029355, -0.0025940043518061524, -0.002493914246284927, -0.002367913967619183, -0.002218049686658729, -0.0020465811515882654, -0.001855957791523151, -0.0016487810144776998, -0.00142777710384698, -0.0011957607970448994, -0.0009556043868967322, -0.0007102032874819869, -0.00046244421208314695, -0.00021517299351677294, 0.00002883562686647948, 0.00026690748187752, 0.0004964962605656626, 0.0007152087484632526, 0.0009208280531856993, 0.0011113341710461287, 0.001284922104875704, 0.001440017221858243, 0.0015752874926775115, 0.001689653007641102, 0.0017822924847919327, 0.0018526466567171573, 0.001900418695963952, 0.0019255717089461943, 0.0019283234769416758, 0.0019091385171741257, 0.0018687174372601382, 0.0018079839052070358, 0.0017280695480315516, 0.0016302968009115559, 0.0015161599108890337, 0.0013873044920201315, 0.0012455057874817628, 0.0010926459700895676, 0.0009306909211412733, 0.0007616662990892915, 0.0005876334577773431, 0.00041066572571757826, 0.0002328247974905868, 0.00005613781437073196, -0.0001174245121751005, -0.0002859689495020168, -0.0004476991452944222, -0.0006009342372185592, -0.0007441242595773033, -0.0008758672627872311, -0.000994915790719297, -0.0011002003122295141, -0.0011908163778121617, -0.0012660583148430655, -0.0013253984546678576, -0.0013685012143196942, -0.001395225943125387, -0.0014056157668337018, -0.0013998954747501482, -0.001378469827779881, -0.0013419124397293153, -0.0012909532205746962, -0.0012264687733368777, -0.0011494712830100603, -0.0010610931779006438, -0.0009625702506836625, -0.000855225949970909, -0.0007404558934504534, -0.0006197108731105526, -0.0004944786417629195, -0.0003662656228678478, -0.00023657966545821663, -0.00010691385041080575, 0.000021269732776830692, 0.00014655630811094485, 0.00026759372492077656, 0.00038310639941104474, 0.0004919079810065394, 0.0005929124336140955, 0.0006851439794862671, 0.0007677461820400234, 0.00083998929562144, 0.0009012758235801954, 0.0009511444883473427, 0.000989272105808993, 0.001015474237183418, 0.001029704649474236, 0.001032052906747118, 0.0010227407683432643, 0.0010021168270535825, 0.0009706493923198387, 0.0009289191850318768, 0.0008776096510962619, 0.000817498097837222, 0.0007494441437311685, 0.0006743792227901712, 0.0005932933417959479, 0.0005072240121419497, 0.000417242110639473, 0.0003244404697876014, 0.00022991990724017595, 0.00013477726342077335, 0.00004009330845272015, -0.0000530794135812432, -0.00014372740877295807, -0.00023088724840840297, -0.00031365558789641864, -0.00039119738433470065, -0.0004627540773883175, -0.0005276507775505978, -0.000585301724233503, -0.0006352149637547267, -0.0006769959128444833, -0.0007103495905249487, -0.0007350820695666818, -0.0007511005127290484, -0.0007584116112520549, -0.0007571194729701421, -0.00074742277626912, -0.0007296101342453403, -0.0007040544378735058, -0.0006712073306869049, -0.0006315928237496245, -0.0005857992578673142, -0.0005344710675331729, -0.00047830108691105684, -0.00041802158263819515, -0.0003543943076738356, -0.00028820198017881244, -0.0002202395317215665, -0.00015130374925648982, -0.00008218491603536522, -0.000013658831150507367, 0.00005352304340437133, 0.00011864041665267685, 0.00018101095571606833, 0.00023999966108502962, 0.00029502115182460564, 0.00034554887777392786, 0.000391116555802778, 0.000431324450055965, 0.00046584063660783586, 0.0004944041835739037, 0.0005168258169870346, 0.0005329890088078192, 0.0005428491632207548, 0.0005464327395366827, 0.0005438352706939971, 0.0005352187121164756, 0.0005208082939190553, 0.0005008883845701094, 0.00047579797516198916, 0.00044592580363879246, 0.00041170480010448157, 0.0003736062688506139, 0.0003321337258089977, 0.0002878165770709132, 0.00024120378709679795, 0.00019285729618983638, 0.00014334539734493274, 0.00009323633379971508, 0.00004309200179747732, -0.000006538129524184674, -0.00005512275851308814, -0.00010215425682824557, -0.0001471537836846092, -0.00018967580918116832, -0.000229312273588053, -0.00026569630476472707, -0.0002985051407756325, -0.00032746269947154865, -0.0003523416566253701, -0.0003729646779954726, -0.0003892052149924187, -0.0004009877671280609, -0.0004082874857247505, -0.00041112935422556683, -0.0004095865011481009, -0.00040377863032597667, -0.0003938684545478567, -0.000380064037607924, -0.00036259769180095337, -0.00034176866086093054, -0.0003178529521717158, -0.00029121116694135965, -0.00026219407114439766, -0.0002311660005961874, -0.00019851985490222583, -0.00016465832424012215, -0.00012998055684633713, -0.00009488375591619706, -0.0000597648435239552, -0.000025015420382794053, 0.000008986141052938425, 0.00004188007983490808, 0.00007332727057153378, 0.0001030103372114418, 0.00013063572285978273, 0.0001559370040308809, 0.0001786783299691074, 0.00019865656863507874, 0.0002157022795080577, 0.00022968003782829373, 0.00024048836740597296, 0.0002480598527099588, 0.0002523615359642444, 0.0002533948480685339, 0.0002511948137689462, 0.00024582879240017197, 0.00023739462261928077, 0.0002260184818303832, 0.00021185289411595253, 0.00019507450362164447, 0.00017588169703929268, 0.00015449231724590354, 0.0001311409039616243, 0.00010607589207618957, 0.0000795567793351373, 0.00005185089553914594, 0.000023230509204295882, -0.0000060300637869522105, -0.000035657434180248525, -0.00006538116402237262, -0.00009493693873815591, -0.000124068295999576, -0.0001525297202780986, -0.00018008768980098334, -0.00020652386291798106, -0.00023163531609170232, -0.00025523791714505067, -0.00027716574592453883, -0.0002972733235857977, -0.0003154355888326931, -0.00033154842010564274, -0.00034552957412866856, -0.00035731795482855553, -0.0003668736040544923, -0.0003741778985872164, -0.0003792324914686392, -0.0003820586817783959, -0.00038269672658097575, -0.00038120443727980227, -0.0003776561552191149, -0.00037214159801174867, -0.0003647639478719413, -0.0003556383621072125, -0.00034489087939824556, -0.00033265659742357157, -0.0003190776369817763, -0.00030430188679278307, -0.000288481701508917, -0.00027177184977021814, -0.00025432781616982985, -0.0002363048394462032, -0.00021785642907628847, -0.00019913243214872875, -0.00018027812546977655, -0.00016143346375442532, -0.00014273141907304482, -0.00012429715414545613, -0.00010624778005518417, -0.00008869100726664171, -0.00007172486047116929, -0.00005543781265924578, -0.000039907391843692994, -0.000025200639048718578, -0.000011374683335187771, 0.0000015250260932436688, 0.000013462253379241917, 0.00002441217206516509, 0.000034358773177863244, 0.00004329622912604799, 0.00005122720702465441, 0.00005816317471750027, 0.0000641230199308996, 0.000069132993436809, 0.00007322560593960072, 0.00007643924515196579, 0.00007881727036824129, 0.00008040712470181444, 0.00008125983301336947, 0.0000814292294889786, 0.00008097125445283343, 0.00007994329085570354, 0.00007840337111312984, 0.00007640968474357385, 0.00007402000644792147, 0.00007129106772373328, 0.00006827813445641724, 0.00006503452939612308, 0.0000616111910251882, 0.00005805642295254431, 0.00005441556426289718, 0.00005073068873056898, 0.00004704050335408969, 0.000043380204546549804, 0.000039781341263945824, 0.00003627190886201023, 0.00003287635226432179, 0.000029615423861973183, 0.000026506378791440255, 0.000023563179035309233, 0.000020796570670036558, 0.000018214288011421873, 0.000015821201495131063, 0.000013619504364333407, 0.000011608996984880698, 0.00000978725611094941, 0.000008150045704110886, 0.000006691315452907781, 0.000005403667066221734, 0.000004278345295781511, 0.000007843720623236043]

input_sample_rate = 128_000
filter_len = len(filter)
channel_bw = 4_000
channel_sample_rate = int(1.28 * channel_bw)
channel_spacing = int(channel_bw / 2)
num_output_channels = int(input_sample_rate / channel_spacing)
decimation_factor = int(input_sample_rate / channel_sample_rate)
polyphase_factor = int(filter_len / num_output_channels)

num_channelised_output_samples = 4096
num_input_samples = int(decimation_factor * (num_channelised_output_samples - 1) + filter_len)

signal_frequency = 1_000
time = linspace(0, num_input_samples * 1/input_sample_rate, num_input_samples)
time_data = [sin(2 * pi * signal_frequency * t) - 1j * cos(2 * pi * signal_frequency * t) for t in time]

filtered_real = convolve([v.real for v in time_data], filter, 'same')
filtered_imag = convolve([v.imag for v in time_data], filter, 'same')
filtered_data = [complex(x,y) for x,y in zip(filtered_real, filtered_imag)]

phase_shift_correction_counter = 0
phase_correction_shift_modder = lcm(num_output_channels, decimation_factor) // decimation_factor
channelised_data = array([])
for i in range(num_channelised_output_samples):
    input_block = time_data[i*decimation_factor:i*decimation_factor + filter_len]
    input_block = [ x*y for x,y in zip(input_block, filter)]
    input_block = array(input_block).reshape((polyphase_factor, num_output_channels)).T
    input_block = input_block.dot(array([1 for i in range(polyphase_factor)]).reshape((polyphase_factor, 1)))

    phase_shift_modifier = (phase_shift_correction_counter % phase_correction_shift_modder) * decimation_factor
    phase_shift_correction_counter += 1
    phase_shift_correction_counter %= phase_correction_shift_modder

    phase_corrected_input = [complex(0,0) for i in range(len(input_block))]
    for output_channel in range(num_output_channels):
        phase_corrected_index = (output_channel + phase_shift_modifier) % num_output_channels
        phase_corrected_input[phase_corrected_index] = input_block[output_channel]

    channelised_samples = fft.fftshift(fft.fft(phase_corrected_input, axis=0)).reshape(64,1)

    channelised_data = vstack([channelised_data, channelised_samples]) if channelised_data.size else channelised_samples

channelised_data = channelised_data.reshape((int(len(channelised_data) / num_output_channels), num_output_channels))
channelised_data = channelised_data.T

fig, ax = plt.subplots(5)

fft_data = fft.fftshift(fft.fft(time_data[0:num_channelised_output_samples]))
freq = linspace(-input_sample_rate/2, input_sample_rate/2, len(fft_data))
filtered_fft_data = fft.fftshift(fft.fft(filtered_data[0:num_channelised_output_samples]))

time = linspace(0, num_input_samples * 1/input_sample_rate, num_channelised_output_samples)
ax[0].plot(time, time_data[0:num_channelised_output_samples])
ax[1].plot(freq, [10*log10(abs(v) / len(fft_data) + float_info.epsilon) for v in fft_data])
ax[2].plot(time, filtered_data[0:num_channelised_output_samples])
ax[3].plot(freq, [10*log10(abs(v) / len(filtered_fft_data) + float_info.epsilon) for v in filtered_fft_data])

for channel_select in range(num_output_channels):
    channel_data = channelised_data[channel_select]
    channel_centre_frequency = channel_select * channel_spacing - input_sample_rate / 2
    channelised_freq = linspace(channel_centre_frequency - channel_sample_rate/2, channel_centre_frequency + channel_sample_rate/2, channelised_data.shape[1])
    ax[4].plot(channelised_freq, [10*log10(abs(v) / channelised_data.shape[1] + float_info.epsilon) for v in fft.fftshift(fft.fft(channel_data, axis=0))])

plt.show()
