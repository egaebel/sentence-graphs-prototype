from graph_to_vector import approximate_sentence_graph_edit_distance
from graph_to_vector import sentence_graph_dissimilarity_embedding
from graph_to_vector import select_prototype_graphs
from sentence_graph import SentenceGraph
from sentence_graph_construction import get_text_sentence_graphs
from sentence_graph_construction import build_deep_sentence_graph
from sentence_graph_reduction import reduce_sentence_graphs
from sentence_graph_io import graphviz_sentence_graph_draw
from sentence_graph_io import load_sentence_graph_from_file
from sentence_graph_io import sentence_graph_draw
from sentence_graph_io import sentence_graph_file_path_from_sentence
from sentence_graph_io import save_sentence_graph_to_file
from sentence_graph_statistics import minimize_blockmodel_and_draw
from sentence_graph_statistics import similarity_test
from sentence_graph_statistics import statistics_experiments
from vector_visualizations import plot_3d_vectors
from wikipedia_client import scrape_wikipedia
from wikipedia_client import scrape_wikipedia_articles
from wiktionary_client import clear_wiktionary_file_locks
from wiktionary_client import WiktionaryClient

from graph_tool import topology

from multiprocessing import cpu_count
from multiprocessing import Lock
from multiprocessing import Manager
from multiprocessing import Pool

from numpy import linalg

import cProfile
import numpy as np
import sys

# Corex imports
#sys.path.insert(1, "../../corex/CorEx")
#from corex import Corex

# STS Dataset imports
sys.path.insert(1, "../../sentence-similarity-datasets/sts-2014")
from sts_loader import get_sts_dataset_names
from sts_loader import load_sts_dataset
from sts_loader import StsDatasetItem

# Sick Dataset imports
sys.path.insert(1, "../../sentence-similarity-datasets/sick")
from sick_loader import load_sick_dataset
from sick_loader import SickDatasetItem


DEBUG_restart_sentence_index = 0

BBC_ARTICLE = """The British Broadcasting Corporation (BBC) is a British public service broadcaster. It is headquartered at Broadcasting House in London, is the world's oldest national broadcasting organisation, and is the largest broadcaster in the world by number of employees, with over 20,950 staff in total, of whom 16,672 are in public sector broadcasting; when part-time, flexible and fixed contract staff are included, the total number is 35,402.The BBC is established under a Royal Charter and operates under its Agreement with the Secretary of State for Culture, Media and Sport. Its work is funded principally by an annual television licence fee which is charged to all British households, companies, and organisations using any type of equipment to receive or record live television broadcasts. The fee is set by the British Government, agreed by Parliament, and used to fund the BBC's radio, TV, and online services covering the nations and regions of the UK. Since 1 April 2014, it has also funded the BBC World Service (launched in 1932 as the BBC Empire Service), which broadcasts in 28 languages and provides comprehensive TV, radio, and online services in Arabic, and Persian.Around a quarter of BBC revenues come from its commercial arm BBC Worldwide Ltd, which sells BBC programmes and services internationally and also distributes the BBC's international 24-hour English-language news services BBC World News, and from BBC.com, provided by BBC Global News Ltd.Britain's first live public broadcast from the Marconi factory in Chelmsford took place in June 1920. It was sponsored by the Daily Mail's Lord Northcliffe and featured the famous Australian Soprano Dame Nellie Melba. The Melba broadcast caught the people's imagination and marked a turning point in the British public's attitude to radio. However, this public enthusiasm was not shared in official circles where such broadcasts were held to interfere with important military and civil communications. By late 1920, pressure from these quarters and uneasiness among the staff of the licensing authority, the General Post Office (GPO), was sufficient to lead to a ban on further Chelmsford broadcasts.But by 1922, the GPO had received nearly 100 broadcast licence requests and moved to rescind its ban in the wake of a petition by 63 wireless societies with over 3,000 members. Anxious to avoid the same chaotic expansion experienced in the United States the GPO proposed that it would issue a single broadcasting licence to a company jointly owned by a consortium of leading wireless receiver manufactures, to be known as the British Broadcasting Company Ltd. John Reith, a Scottish Calvinist, was appointed its General Manager in December 1922 a few weeks after the company made its first official broadcast. The company was to be financed by a royalty on the sale of BBC wireless receiving sets from approved manufacturers. To this day, the BBC aims to follow the Reithian directive to "inform, educate and entertain".The financial arrangements soon proved inadequate. Set sales were disappointing as amateurs made their own receivers and listeners bought rival unlicensed sets. By mid-1923, discussions between the GPO and the BBC had become deadlocked and the Postmaster-General commissioned a review of broadcasting by the Sykes Committee. The Committee recommended a short term reorganisation of licence fees with improved enforcement in order to address the BBC's immediate financial distress, and an increased share of the licence revenue split between it and the GPO. This was to be followed by a simple 10 shillings licence fee with no royalty once the wireless manufactures protection expired. The BBC's broadcasting monopoly was made explicit for the duration of its current broadcast licence, as was the prohibition on advertising. The BBC was also banned from presenting news bulletins before 19.00, and required to source all news from external wire services.Mid-1925 found the future of broadcasting under further consideration, this time by the Crawford committee. By now the BBC under Reith's leadership had forged a consensus favouring a continuation of the unified (monopoly) broadcasting service, but more money was still required to finance rapid expansion. Wireless manufacturers were anxious to exit the loss making consortium with Reith keen that the BBC be seen as a public service rather than a commercial enterprise. The recommendations of the Crawford Committee were published in March the following year and were still under consideration by the GPO when the 1926 general strike broke out in May. The strike temporarily interrupted newspaper production and with restrictions on news bulletins waived the BBC suddenly became the primary source of news for the duration of the crisis.The crisis placed the BBC in a delicate position. On one hand Reith was acutely aware that the Government might exercise its right to commandeer the BBC at any time as a mouthpiece of the Government if the BBC were to step out of line, but on the other he was anxious to maintain public trust by appearing to be acting independently. The Government was divided on how to handle the BBC but ended up trusting Reith, whose opposition to the strike mirrored the PM's own. Thus the BBC was granted sufficient leeway to pursue the Government's objectives largely in a manner of its own choosing. The resulting coverage of both striker and government viewpoints impressed millions of listeners who were unaware that the PM had broadcast to the nation from Reith's home, using one of Reith's sound bites inserted at the last moment, or that the BBC had banned broadcasts from the Labour Party and delayed a peace appeal by the Archbishop of Canterbury. Supporters of the strike nicknamed the BBC the BFC for British Falsehood Company. Reith personally announced the end of the strike which he marked by reciting from Blake's "Jerusalem" signifying that England had been saved.While the BBC tends to characterise its coverage of the general strike by emphasising the positive impression created by its balanced coverage of the views of government and strikers, Jean Seaton, Professor of Media History and the Official BBC Historian has characterised the episode as the invention of "modern propaganda in its British form". Reith argued that trust gained by 'authentic impartial news' could then be used. Impartial news was not necessarily an end in itself.The BBC did well out of the crisis, which cemented a national audience for its broadcasting, and it was followed by the Government's acceptance of the recommendation made by the Crawford Committee (1925-26) that the British Broadcasting Company be replaced by a non-commercial, Crown-chartered organisation: the British Broadcasting Corporation.The British Broadcasting Corporation came into existence on 1 January 1927, and Reith - newly knighted - was appointed its first Director General. To represent its purpose and (stated) values, the new corporation adopted the coat of arms, including the motto "Nation shall speak peace unto Nation".British radio audiences had little choice apart from the upscale programming of the BBC. Reith, an intensely moralistic executive, was in full charge. His goal was to broadcast, "All that is best in every department of human knowledge, endeavour and achievement.... The preservation of a high moral tone is obviously of paramount importance." Reith succeeded in building a high wall against an American-style free-for-all in radio in which the goal was to attract the largest audiences and thereby secure the greatest advertising revenue. There was no paid advertising on the BBC; all the revenue came from a tax on receiving sets. Highbrow audiences, however, greatly enjoyed it. At a time when American, Australian and Canadian stations were drawing huge audiences cheering for their local teams with the broadcast of baseball, rugby and hockey, the BBC emphasized service for a national, rather than a regional audience. Boat races were well covered along with tennis and horse racing, but the BBC was reluctant to spend its severely limited air time on long football or cricket games, regardless of their popularity.The success of broadcasting provoked animosities between the BBC and well established media such as theatres, concert halls and the recording industry. By 1929, the BBC complained that the agents of many comedians refused to sign contracts for broadcasting, because they feared it harmed the artist "by making his material stale" and that it "reduces the value of the artist as a visible music-hall performer". On the other hand, the BBC was "keenly interested" in a cooperation with the recording companies who "in recent years ... have not been slow to make records of singers, orchestras, dance bands, etc. who have already proved their power to achieve popularity by wireless." Radio plays were so popular that the BBC had received 6,000 manuscripts by 1929, most of them written for stage and of little value for broadcasting: "Day in and day out, manuscripts come in, and nearly all go out again through the post, with a note saying 'We regret, etc.'" In the 1930s music broadcasts also enjoyed great popularity, for example the friendly and wide-ranging organ broadcasts at St George's Hall, Langham Place, by Reginald Foort, who held the official role of BBC Staff Theatre Organist from 1936 to 1938; Foort continued to work for the BBC as a freelance into the 1940s and enjoyed a nationwide following.Experimental television broadcasts were started in 1932, using an electromechanical 30-line system developed by John Logie Baird. Limited regular broadcasts using this system began in 1934, and an expanded service (now named the BBC Television Service) started from Alexandra Palace in 1936, alternating between an improved Baird mechanical 240 line system and the all electronic 405 line Marconi-EMI system. The superiority of the electronic system saw the mechanical system dropped early the following year.Television broadcasting was suspended from 1 September 1939 to 7 June 1946, during the Second World War, and it was left to BBC Radio broadcasters such as Reginald Foort to keep the nation's spirits up. The BBC moved much of its radio operations out of London, initially to Bristol, and then to Bedford. Concerts were broadcast from the Corn Exchange; the Trinity Chapel in St Paul's Church, Bedford was the studio for the daily service from 1941 to 1945 and, in the darkest days of the war in 1941, the Archbishops of Canterbury and York came to St Paul's to broadcast to the UK and all parts of the world on the National Day of Prayer.There was a widely reported urban myth that, upon resumption of the BBC television service after the war, announcer Leslie Mitchell started by saying, "As I was saying before we were so rudely interrupted ..." In fact, the first person to appear when transmission resumed was Jasmine Bligh and the words said were "Good afternoon, everybody. How are you? Do you remember me, Jasmine Bligh ... ?"The European Broadcasting Union was formed on 12 February 1950, in Torquay with the BBC among the 23 founding broadcasting organisations.Competition to the BBC was introduced in 1955, with the commercial and independently operated television network of ITV. However, the BBC monopoly on radio services would persist until 8 October 1973 when under the control of the newly renamed Independent Broadcasting Authority (IBA) the UK's first Independent local radio station, LBC came on-air in the London area. As a result of the Pilkington Committee report of 1962, in which the BBC was praised for the quality and range of its output, and ITV was very heavily criticised for not providing enough quality programming, the decision was taken to award the BBC a second television channel, BBC2, in 1964, renaming the existing service BBC1. BBC2 used the higher resolution 625 line standard which had been standardised across Europe. BBC2 was broadcast in colour from 1 July 1967, and was joined by BBC1 and ITV on 15 November 1969. The 405 line VHF transmissions of BBC1 (and ITV) were continued for compatibility with older television receivers until 1985.Starting in 1964, a series of pirate radio stations (starting with Radio Caroline) came on the air and forced the British government finally to regulate radio services to permit nationally based advertising-financed services. In response, the BBC reorganised and renamed their radio channels. On 30 September 1967, the Light Programme was split into Radio 1 offering continuous "Popular" music and Radio 2 more "Easy Listening". The "Third" programme became Radio 3 offering classical music and cultural programming. The Home Service became Radio 4 offering news, and non-musical content such as quiz shows, readings, dramas and plays. As well as the four national channels, a series of local BBC radio stations were established in 1967, including Radio London.In 1969, the BBC Enterprises department was formed to exploit BBC brands and programmes for commercial spin-off products. In 1979, it became a wholly owned limited company, BBC Enterprises Ltd.In 1974, the BBC's teletext service, Ceefax, was introduced, created initially to provide subtitling, but developed into a news and information service. In 1978, BBC staff went on strike just before the Christmas of that year, thus blocking out the transmission of both channels and amalgamating all four radio stations into one.Since the deregulation of the UK television and radio market in the 1980s, the BBC has faced increased competition from the commercial sector (and from the advertiser-funded public service broadcaster Channel 4), especially on satellite television, cable television, and digital television services.[citation needed]In the late 1980s, the BBC began a process of divestment by spinning off and selling parts of its organisation. In 1988, it sold off the Hulton Press Library, a photographic archive which had been acquired from the Picture Post magazine by the BBC in 1957. The archive was sold to Brian Deutsch and is now owned by Getty Images. During the 1990s, this process continued with the separation of certain operational arms of the corporation into autonomous but wholly owned subsidiaries of the BBC, with the aim of generating additional revenue for programme-making. BBC Enterprises was reorganised and relaunched in 1995, as BBC Worldwide Ltd. In 1998, BBC studios, outside broadcasts, post production, design, costumes and wigs were spun off into BBC Resources Ltd.The BBC Research Department has played a major part in the development of broadcasting and recording techniques. In the early days, it carried out essential research into acoustics and programme level and noise measurement.[citation needed] The BBC was also responsible for the development of the NICAM stereo standard.In recent decades, a number of additional channels and radio stations have been launched: Radio 5 was launched in 1990, as a sports and educational station, but was replaced in 1994, with Radio 5 Live, following the success of the Radio 4 service to cover the 1991 Gulf War. The new station would be a news and sport station. In 1997, BBC News 24, a rolling news channel, launched on digital television services and the following year, BBC Choice launched as the third general entertainment channel from the BBC. The BBC also purchased The Parliamentary Channel, which was renamed BBC Parliament. In 1999, BBC Knowledge launched as a multi media channel, with services available on the newly launched BBC Text digital teletext service, and on BBC Online. The channel had an educational aim, which was modified later on in its life to offer documentaries.In 2002, several television and radio channels were reorganised. BBC Knowledge was replaced by BBC Four and became the BBC's arts and documentaries channel. CBBC, which had been a programming strand as Children's BBC since 1985, was split into CBBC and CBeebies, for younger children, with both new services getting a digital channel: the CBBC Channel and CBeebies Channel. In addition to the television channels, new digital radio stations were created: 1Xtra, 6 Music and BBC7. BBC 1Xtra was a sister station to Radio 1 and specialised in modern black music, BBC 6 Music specialised in alternative music genres and BBC7 specialised in archive, speech and children's programming.The following few years resulted in repositioning of some of the channels to conform to a larger brand: in 2003, BBC Choice was replaced by BBC Three, with programming for younger generations and shocking real life documentaries, BBC News 24 became the BBC News Channel in 2008, and BBC Radio 7 became BBC Radio 4 Extra in 2011, with new programmes to supplement those broadcast on Radio 4. In 2008, another channel was launched, BBC Alba, a Scottish Gaelic service.During this decade, the corporation began to sell off a number of its operational divisions to private owners; BBC Broadcast was spun off as a separate company in 2002, and in 2005. it was sold off to Australian-based Macquarie Capital Alliance Group and Macquarie Bank Limited and rebranded Red Bee Media. The BBC's IT, telephony and broadcast technology were brought together as BBC Technology Ltd in 2001, and the division was later sold to the German engineering and electronics company Siemens IT Solutions and Services (SIS). SIS was subsequently acquired from Siemens by the French company Atos. Further divestments in this decade included BBC Books (sold to Random House in 2006); BBC Outside Broadcasts Ltd (sold in 2008. to Satellite Information Services); Costumes and Wigs (stock sold in 2008 to Angels The Costumiers); and BBC Magazines (sold to Immediate Media Company in 2011). After the sales of OBs and costumes, the remainder of BBC Resources was reorganised as BBC Studios and Post Production, which continues today as a wholly owned subsidiary of the BBC.The 2004 Hutton Inquiry and the subsequent Report raised questions about the BBC's journalistic standards and its impartiality. This led to resignations of senior management members at the time including the then Director General, Greg Dyke. In January 2007, the BBC released minutes of the board meeting which led to Greg Dyke's resignation.Unlike the other departments of the BBC, the BBC World Service was funded by the Foreign and Commonwealth Office. The Foreign and Commonwealth Office, more commonly known as the Foreign Office or the FCO, is the British government department responsible for promoting the interests of the United Kingdom abroad.In 2006, BBC HD launched as an experimental service, and became official in December 2007. The channel broadcast HD simulcasts of programmes on BBC One, BBC Two, BBC Three and BBC Four as well as repeats of some older programmes in HD. In 2010, an HD simulcast of BBC One launched: BBC One HD. The channel uses HD versions of BBC One's schedule and uses upscaled versions of programmes not currently produced in HD. The BBC HD channel closed in March 2013 and was replaced by BBC2 HD in the same month.On 18 October 2007, BBC Director General Mark Thompson announced a controversial plan to make major cuts and reduce the size of the BBC as an organisation. The plans included a reduction in posts of 2,500; including 1,800 redundancies, consolidating news operations, reducing programming output by 10% and selling off the flagship Television Centre building in London. These plans have been fiercely opposed by unions, who have threatened a series of strikes; however, the BBC have stated that the cuts are essential to move the organisation forward and concentrate on increasing the quality of programming.On 20 October 2010, the Chancellor of the Exchequer George Osborne announced that the television licence fee would be frozen at its current level until the end of the current charter in 2016. The same announcement revealed that the BBC would take on the full cost of running the BBC World Service and the BBC Monitoring service from the Foreign and Commonwealth Office, and partially finance the Welsh broadcaster S4C.Further cuts were announced on 6 October 2011, so the BBC could reach a total reduction in their budget of 20%, following the licence fee freeze in October 2010, which included cutting staff by 2,000 and sending a further 1,000 to the MediaCityUK development in Salford, with BBC Three moving online only in 2016, the sharing of more programmes between stations and channels, sharing of radio news bulletins, more repeats in schedules, including the whole of BBC Two daytime and for some original programming to be reduced. BBC HD was closed on 26 March 2013, and replaced with an HD simulcast of BBC Two; however, flagship programmes, other channels and full funding for CBBC and CBeebies would be retained. Numerous BBC facilities have been sold off, including New Broadcasting House on Oxford Road in Manchester. Many major departments have been relocated to Broadcasting House and MediaCityUK, particularly since the closure of BBC Television Centre in March 2013. The cuts inspired campaigns, petitions and protests such as SaveBBC3 and SaveOurBBC, which have built a following of hundreds of thousands of individuals concerned about the changes.The BBC is a statutory corporation, independent from direct government intervention, with its activities being overseen by the BBC Trust (formerly the Board of Governors). General management of the organisation is in the hands of a Director-General, appointed by the Trust, who is the BBC's Editor-in-Chief and chairs the Executive Board.The BBC operates under a Royal Charter. The current Charter came into effect on 1 January 2007 and runs until 31 December 2016. Each successive Royal Charter is reviewed before a new one is granted, i.e. every 10 years.The 2007 Charter specifies that the mission of the Corporation is to "inform, educate and entertain". It states that the Corporation exists to serve the public interest and to promote its public purposes: sustaining citizenship and civil society, promoting education and learning, stimulating creativity and cultural excellence, representing the UK, its nations, regions and communities, bringing the UK to the world and the world to the UK, helping to deliver to the public the benefit of emerging communications technologies and services, and taking a leading role in the switchover to digital television.The 2007 Charter made the largest change in the governance of the Corporation since its inception. It abolished the sometimes controversial governing body, the Board of Governors, replacing it with the sometimes controversial BBC Trust and a formalised Executive Board.Under the Royal Charter, the BBC must obtain a licence from the Home Secretary. This licence is accompanied by an agreement which sets the terms and conditions under which the BBC is allowed to broadcast. It was under this Licence and Agreement (and the Broadcasting Act 1981) that the Sinn F in broadcast ban from 1988 to 1994 was implemented.The BBC Trust was formed on 1 January 2007, replacing the Board of Governors as the governing body of the Corporation. The Trust sets the strategy for the corporation, assesses the performance of the BBC Executive Board in delivering the BBC's services, and appoints the Director-General.BBC Trustees are appointed by the British monarch on advice of government ministers. There are twelve trustees, led by Chairman Rona Fairhead who was appointed on 31 August 2014 and vice-chairman Sir Roger Carr. There are trustees for the four nations of the United Kingdom; England (Mark Florman), Scotland (Bill Matthews), Wales (Elan Closs Stephens) and Northern Ireland (Aideen McGinley). The remaining trustees are Sonita Alleyne, Richard Ayre, Mark Damazer, Nicholas Prettejohn, Suzanna Taverne and Lord Williams.The Executive Board meets once per month and is responsible for operational management and delivery of services within a framework set by the BBC Trust, and is headed by the Director-General, currently Tony Hall. The Executive Board consists of both Executive and Non-Executive directors, with non-executive directors being sourced from other companies and corporations and being appointed by the BBC Trust. The executive board is made up of the Director General as well as the head of each of the main BBC divisions. These at present are:The board shares some of its responsibilities to four sub-committees including: Audit, Fair Trading, Nominations and Remuneration.It is also supported by a number of management groups within the BBC, including the BBC Management Board, the Finance and Business committee, and boards at the Group level, such as Radio and Television. The boards of BBC Worldwide support and BBC Commercial Holdings along with the Executive Board on commercial matters.The management board is responsible for managing pan-BBC issues delegated to it from the executive board and ensures that the corporation meets its strategic objectives, the board meets three times per month. Current members include:The Corporation is headed by the Executive Board, which has overall control of the management and running of the BBC. Below this is the BBC Management board, which deals with inter departmental issues and any other tasks which the Executive board has delegated to it. Below the BBC Management board are the following six major divisions covering all the BBC's output:All aspects of the BBC fall into one or more of the above departments, with the following exceptions:The BBC has the second largest budget of any UK-based broadcaster with an operating expenditure of  4.722 billion in 2013/14 compared to  6.471 billion for British Sky Broadcasting in 2013/14 and  1.843 billion for ITV in the calendar year 2013.The principal means of funding the BBC is through the television licence, costing  145.50 per year per household since April 2010. Such a licence is required to legally receive broadcast television across the UK, the Channel Islands and the Isle of Man. No licence is required to own a television used for other means, or for sound only radio sets (though a separate licence for these was also required for non-TV households until 1971). The cost of a television licence is set by the government and enforced by the criminal law. A discount is available for households with only black-and-white television sets. A 50% discount is also offered to people who are registered blind or severely visually impaired, and the licence is completely free for any household containing anyone aged 75 or over. As a result of the UK Government's recent spending review, an agreement has been reached between the government and the corporation in which the current licence fee will remain frozen at the current level until the Royal Charter is renewed at the beginning of 2017.The revenue is collected privately[clarification needed] and is paid into the central government Consolidated Fund, a process defined in the Communications Act 2003. The BBC pursues its licence fee collection and enforcement under the trading name "TV Licensing". TV Licensing collection is currently carried out by Capita, an outside agency. Funds are then allocated by the Department of Culture, Media and Sport (DCMS) and the Treasury and approved by Parliament via legislation. Additional revenues are paid by the Department for Work and Pensions to compensate for subsidised licences for eligible over-75-year-olds.The licence fee is classified as a tax, and its evasion is a criminal offence. Since 1991, collection and enforcement of the licence fee has been the responsibility of the BBC in its role as TV Licensing Authority. Thus, the BBC is a major prosecuting authority in England and Wales and an investigating authority in the UK as a whole. The BBC carries out surveillance (mostly using subcontractors) on properties (under the auspices of the Regulation of Investigatory Powers Act 2000) and may conduct searches of a property using a search warrant. According to the BBC, "more than 204,000 people in the UK were caught watching TV without a licence during the first six months of 2012." Licence fee evasion makes up around one tenth of all cases prosecuted in magistrate courts.Income from commercial enterprises and from overseas sales of its catalogue of programmes has substantially increased over recent years, with BBC Worldwide contributing some  145 million to the BBC's core public service business.According to the BBC's 2013/14 Annual Report, its total income was  5 billion ( 5.066 billion), which can be broken down as follows:The licence fee has, however, attracted criticism. It has been argued that in an age of multi stream, multi-channel availability, an obligation to pay a licence fee is no longer appropriate. The BBC's use of private sector company Capita Group to send letters to premises not paying the licence fee has been criticised, especially as there have been cases where such letters have been sent to premises which are up to date with their payments, or do not require a TV licence.The BBC uses advertising campaigns to inform customers of the requirement to pay the licence fee. Past campaigns have been criticised by Conservative MP Boris Johnson and former MP Ann Widdecombe, for having a threatening nature and language used to scare evaders into paying. Audio clips and television broadcasts are used to inform listeners of the BBC's comprehensive database. There are a number of pressure groups campaigning on the issue of the licence fee.The majority of the BBC's commercial output comes from its commercial arm BBC Worldwide who sell programmes abroad and exploit key brands for merchandise. Of their 2012/13 sales, 27% were centred on the five key 'superbrands' of Doctor Who, Top Gear, Strictly Come Dancing (known as Dancing with the Stars internationally), the BBC's archive of natural history programming (collected under the umbrella of BBC Earth) and the, now sold, travel guide brand Lonely Planet.The following expenditure figures are from 2012/13 and show the expenditure of each service they are obliged to provide:A significantly large portion of the BBC's income is spent on the corporation's Television and Radio services with each service having a different budget based upon their content.Broadcasting House in Portland Place, London, is the official headquarters of the BBC. It is home to six of the ten BBC national radio networks, BBC Radio 1, BBC Radio 1xtra, BBC Asian Network, BBC Radio 3, BBC Radio 4, and BBC Radio 4 Extra. It is also the home of BBC News, which relocated to the building from BBC Television Centre in 2013. On the front of the building are statues of Prospero and Ariel, characters from William Shakespeare's play The Tempest, sculpted by Eric Gill. Renovation of Broadcasting House began in 2002, and was completed in 2013.Until it closed at the end of March 2013, BBC Television was based at BBC Television Centre, a purpose built television facility and the second built in the country located in White City, London. This facility has been host to a number of famous guests and programmes through the years, and its name and image is familiar with many British citizens. Nearby, the BBC White City complex contains numerous programme offices, housed in Centre House, the Media Centre and Broadcast Centre. It is in this area around Shepherd's Bush that the majority of BBC employees work.As part of a major reorganisation of BBC property, the entire BBC News operation relocated from the News Centre at BBC Television Centre to the refurbished Broadcasting House to create what is being described as "one of the world's largest live broadcast centres". The BBC News Channel and BBC World News relocated to the premises in early 2013. Broadcasting House is now also home to most of the BBC's national radio stations, and the BBC World Service. The major part of this plan involves the demolition of the two post-war extensions to the building and construction of an extension designed by Sir Richard MacCormac of MJP Architects. This move will concentrate the BBC's London operations, allowing them to sell Television Centre, which is expected to be completed by 2016.In addition to the scheme above, the BBC is in the process of making and producing more programmes outside London, involving production centres such as Belfast, Cardiff, Glasgow and, most notably, in Greater Manchester as part of the 'BBC North Project' scheme where several major departments, including BBC North West, BBC Manchester, BBC Sport, BBC Children's, CBeebies, Radio 5 Live, BBC Radio 5 Live Sports Extra, BBC Breakfast, BBC Learning and the BBC Philharmonic have all moved from their previous locations in either London or New Broadcasting House, Manchester to the new 200-acre (80ha) MediaCityUK production facilities in Salford, that form part of the large BBC North Group division and will therefore become the biggest staffing operation outside London.As well as the two main sites in London (Broadcasting House and White City), there are seven other important BBC production centres in the UK, mainly specialising in different productions. Broadcasting House Cardiff, has been home to BBC Cymru Wales, which specialises in drama production. Open since October 2011, and containing 7 new studios, Roath Lock is notable as the home of productions such as Doctor Who and Casualty. Broadcasting House Belfast, home to BBC Northern Ireland, specialises in original drama and comedy, and has taken part in many co-productions with independent companies and notably with RT  in the Republic of Ireland. BBC Scotland, based in Pacific Quay, Glasgow is a large producer of programmes for the network, including several quiz shows. In England, the larger regions also produce some programming.Previously, the largest 'hub' of BBC programming from the regions is BBC North West. At present they produce all Religious and Ethical programmes on the BBC, as well as other programmes such as A Question of Sport. However, this is to be merged and expanded under the BBC North project, which involved the region moving from New Broadcasting House, Manchester, to MediaCityUK. BBC Midlands, based at The Mailbox in Birmingham, also produces drama and contains the headquarters for the English regions and the BBC's daytime output. Other production centres include Broadcasting House Bristol, home of BBC West and famously the BBC Natural History Unit and to a lesser extent, Quarry Hill in Leeds, home of BBC Yorkshire. There are also many smaller local and regional studios throughout the UK, operating the BBC regional television services and the BBC Local Radio stations.The BBC also operates several news gathering centres in various locations around the world, which provide news coverage of that region to the national and international news operations.In 2004, the BBC contracted out its former BBC Technology division to the German engineering and electronics company Siemens IT Solutions and Services (SIS), outsourcing its IT, telephony and broadcast technology systems. When Atos Origin acquired the SIS division from Siemens in December 2010 for  850 million ( 720m), the BBC support contract also passed to Atos, and in July 2011, the BBC announced to staff that its technology support would become an Atos service. Siemens staff working on the BBC contract were transferred to Atos and BBC technology systems (including the BBC website) are now managed by Atos. In 2011, the BBC's Chief Financial Officer Zarin Patel stated to the House of Commons Public Accounts Committee that, following criticism of the BBC's management of major IT projects with Siemens (such as the Digital Media Initiative), the BBC partnership with Atos would be instrumental in achieving cost savings of around  64 million as part of the BBC's "Delivering Quality First" programme. In 2012, the BBC's Chief Technology Officer, John Linwood, expressed confidence in service improvements to the BBC's technology provision brought about by Atos. He also stated that supplier accountability had been strengthened following some high-profile technology failures which had taken place during the partnership with Siemens.The BBC operates several television channels in the UK of which BBC One and BBC Two are the flagship television channels. In addition to these two flagship channels, the BBC operates several digital only stations: BBC Four, BBC News, BBC Parliament, and two children's channels, CBBC and CBeebies. Digital television is now in widespread use in the UK, with analogue transmission completely phased out by December 2012. It also operates the internet television service BBC Three, which ceased broadcasting as a linear television channel in February 2016.BBC One is a regionalised TV service which provides opt-outs throughout the day for local news and other local programming. These variations are more pronounced in the BBC 'Nations', i.e. Northern Ireland, Scotland and Wales, where the presentation is mostly carried out locally on BBC One and Two, and where programme schedules can vary largely from that of the network. BBC Two variations exist in the Nations; however, English regions today rarely have the option to 'opt out' as regional programming now only exists on BBC One, and regional opt outs are not possible in the regions that have already undertaken the switch to digital television. BBC Two was also the first channel to be transmitted on 625 lines in 1964, then carry a small-scale regular colour service from 1967. BBC One would follow in November 1969.A new Scottish Gaelic television channel, BBC Alba, was launched in September 2008. It is also the first multi-genre channel to come entirely from Scotland with almost all of its programmes made in Scotland. The service was initially only available via satellite but since June 2011 has been available to viewers in Scotland on Freeview and cable television.The BBC currently operates HD simulcasts of all its nationwide channels with the exception of BBC Parliament. Until 26 March 2013, a separate channel called BBC HD was available, in place of BBC Two HD. It launched on 9 June 2006, following a 12-month trial of the broadcasts. It became a proper channel in 2007, and screened HD programmes as simulcasts of the main network, or as repeats. The corporation has been producing programmes in the format for many years, and stated that it hoped to produce 100% of new programmes in HDTV by 2010. On 3 November 2010, a high-definition simulcast of BBC One was launched, entitled BBC One HD, and BBC Two HD launched on 26 March 2013, replacing BBC HD.In the Republic of Ireland, Belgium, the Netherlands and Switzerland, the BBC channels are available in a number of ways. In these countries digital and cable operators carry a range of BBC channels. These include BBC One, BBC Two and BBC World News, although viewers in the Republic of Ireland may receive BBC services via 'overspill' from transmitters in Northern Ireland or Wales, or via 'deflectors' - transmitters in the Republic which rebroadcast broadcasts from the UK, received off-air, or from digital satellite.Since 1975, the BBC has also provided its TV programmes to the British Forces Broadcasting Service (BFBS), allowing members of UK military serving abroad to watch them on four dedicated TV channels. From 27 March 2013, BFBS will carry versions of BBC One and BBC Two, which will include children's programming from CBBC, as well as carrying programming from BBC Three on a new channel called BFBS Extra.Since 2008, all the BBC channels are available to watch online through the BBC iPlayer service. This online streaming ability came about following experiments with live streaming, involving streaming certain channels in the UK.In February 2014, Director-General Tony Hall announced that the corporation needed to save  100 million. In March 2014, the BBC confirmed plans for BBC Three to become an internet-only channel.In December 2012, the BBC completed a digitisation exercise, scanning the listings of all BBC programmes from an entire run of about 4,500 copies of the Radio Times magazine from the first, 1923, issue to 2009 (later listings already being held electronically), the 'BBC Genome project', with a view to creating an online database of its programme output. An earlier ten months of listings are to be obtained from other sources. They identified around five million programmes, involving 8.5 million actors, presenters, writers and technical staff. The Genome project was opened to public access on 15 October 2014, with corrections to OCR errors and changes to advertised schedules being crowdsourced.The BBC has ten radio stations serving the whole of the UK, a further six stations in the "national regions" (Wales, Scotland, and Northern Ireland), and 40 other local stations serving defined areas of England. Of the ten national stations, five are major stations and are available on FM and/or AM as well as on DAB and online. These are BBC Radio 1, offering new music and popular styles and being notable for its chart show; BBC Radio 2, playing Adult contemporary, country and soul music amongst many other genres; BBC Radio 3, presenting classical and jazz music together with some spoken-word programming of a cultural nature in the evenings; BBC Radio 4, focusing on current affairs, factual and other speech-based programming, including drama and comedy; and BBC Radio 5 Live, broadcasting 24-hour news, sport and talk programmes.In addition to these five stations, the BBC also runs a further five stations that broadcast on DAB and online only. These stations supplement and expand on the big five stations, and were launched in 2002. BBC Radio 1Xtra sisters Radio 1, and broadcasts new black music and urban tracks. BBC Radio 5 Live Sports Extra sisters 5 Live and offers extra sport analysis, including broadcasting sports that previously were not covered. BBC Radio 6 Music offers alternative music genres and is notable as a platform for new artists.BBC Radio 7, later renamed BBC Radio 4 Extra, provided archive drama, comedy and children's programming. Following the change to Radio 4 Extra, the service has dropped a defined children's strand in favour of family-friendly drama and comedy. In addition, new programmes to complement Radio 4 programmes were introduced such as Ambridge Extra, and Desert Island Discs revisited. The final station is the BBC Asian Network, providing music, talk and news to this section of the community. This station evolved out of Local radio stations serving certain areas, and as such this station is available on Medium Wave frequency in some areas of the Midlands.As well as the national stations, the BBC also provides 40 BBC Local Radio stations in England and the Channel Islands, each named for and covering a particular city and its surrounding area (e.g. BBC Radio Bristol), county or region (e.g. BBC Three Counties Radio), or geographical area (e.g. BBC Radio Solent covering the central south coast). A further six stations broadcast in what the BBC terms "the national regions": Wales, Scotland, and Northern Ireland. These are BBC Radio Wales (in English), BBC Radio Cymru (in Welsh), BBC Radio Scotland (in English), BBC Radio nan Gaidheal (in Scottish Gaelic), BBC Radio Ulster, and BBC Radio Foyle, the latter being an opt-out station from Radio Ulster for the north-west of Northern Ireland.The BBC's UK national channels are also broadcast in the Channel Islands and the Isle of Man (although these Crown dependencies are outside the UK), and in the former there are two local stations - BBC Guernsey and BBC Radio Jersey. There is no BBC local radio station, however, in the Isle of Man, partly because the island has long been served by the popular independent commercial station, Manx Radio, which predates the existence of BBC Local Radio. BBC services in the dependencies are financed from television licence fees which are set at the same level as those payable in the UK, although collected locally. This is the subject of some controversy in the Isle of Man since, as well as having no BBC Local Radio service, the island also lacks a local television news service analogous to that provided by BBC Channel Islands.For a worldwide audience, the BBC World Service provides news, current affairs and information in 28 languages, including English, around the world and is available in over 150 capital cities. It is broadcast worldwide on shortwave radio, DAB and online and has an estimated weekly audience of 192 million, and its websites have an audience of 38 million people per week. Since 2005, it is also available on DAB in the UK, a step not taken before, due to the way it is funded. The service is funded by a Parliamentary Grant-in-Aid, administered by the Foreign Office; however, following the Government's spending review in 2011, this funding will cease, and it will be funded for the first time through the Licence fee. In recent years, some services of the World Service have been reduced; the Thai service ended in 2006, as did the Eastern European languages, with resources diverted instead into the new BBC Arabic  the BBC was the only legal radio broadcaster based in the UK mainland until 1967, when University Radio York (URY), then under the name Radio York, was launched as the first, and now oldest, legal independent radio station in the country. However, the BBC did not enjoy a complete monopoly before this as several Continental stations, such as Radio Luxembourg, had broadcast programmes in English to Britain since the 1930s and the Isle of Man-based Manx Radio began in 1964. Today, despite the advent of commercial radio, BBC radio stations remain among the most listened to in the country, with Radio 2 having the largest audience share (up to 16.8% in 2011-12) and Radios 1 and 4 ranked second and third in terms of weekly reach.BBC programming is also available to other services and in other countries. Since 1943, the BBC has provided radio programming to the British Forces Broadcasting Service, which broadcasts in countries where British troops are stationed. BBC Radio 1 is also carried in the United States and Canada on Sirius XM Radio (online streaming only).The BBC is a patron of The Radio Academy.BBC News is the largest broadcast news gathering operation in the world, providing services to BBC domestic radio as well as television networks such as the BBC News, BBC Parliament and BBC World News. In addition to this, news stories are available on the BBC Red Button service and BBC News Online. In addition to this, the BBC has been developing new ways to access BBC News, as a result has launched the service on BBC Mobile, making it accessible to mobile phones and PDAs, as well as developing alerts by e-mail, digital television, and on computers through a desktop alert.Ratings figures suggest that during major incidents such as the 7 July 2005 London bombings or royal events, the UK audience overwhelmingly turns to the BBC's coverage as opposed to its commercial rivals. On 7 July 2005, the day that there were a series of coordinated bomb blasts on London's public transport system, the BBC Online website recorded an all time bandwidth peak of 11 Gb/s at 12.00 on 7 July. BBC News received some 1 billion total hits on the day of the event (including all images, text and HTML), serving some 5.5 terabytes of data. At peak times during the day there were 40,000 page requests per second for the BBC News website. The previous day's announcement of the 2012 Olympics being awarded to London caused a peak of around 5 Gbit/s. The previous all-time high at BBC Online was caused by the announcement of the Michael Jackson verdict, which used 7.2 Gbit/s.The BBC's online presence includes a comprehensive news website and archive. It was launched as BBC Online, before being renamed BBCi, then bbc.co.uk, before it was rebranded back as BBC Online. The website is funded by the Licence fee, but uses GeoIP technology, allowing advertisements to be carried on the site when viewed outside of the UK. The BBC claims the site to be "Europe's most popular content-based site" and states that 13.2 million people in the UK visit the site's more than two million pages each day. According to Alexa's TrafficRank system, in July 2008 BBC Online was the 27th most popular English Language website in the world, and the 46th most popular overall.The centre of the website is the Homepage, which features a modular layout. Users can choose which modules, and which information, is displayed on their homepage, allowing the user to customise it. This system was first launched in December 2007, becoming permanent in February 2008, and has undergone a few aesthetical changes since then. The Homepage then has links to other micro-sites, such as BBC News Online, Sport, Weather, TV and Radio. As part of the site, every programme on BBC Television or Radio is given its own page, with bigger programmes getting their own micro-site, and as a result it is often common for viewers and listeners to be told website addresses (URLs) for the programme website.Another large part of the site also allows users to watch and listen to most Television and Radio output live and for seven days after broadcast using the BBC iPlayer platform, which launched on 27 July 2007, and initially used peer-to-peer and DRM technology to deliver both radio and TV content of the last seven days for offline use for up to 30 days, since then video is now streamed directly. Also, through participation in the Creative Archive Licence group, bbc.co.uk allowed legal downloads of selected archive material via the internet.The BBC has often included learning as part of its online service, running services such as BBC Jam, Learning Zone Class Clips and also runs services such as BBC WebWise and First Click which are designed to teach people how to use the internet. BBC Jam was a free online service, delivered through broadband and narrowband connections, providing high-quality interactive resources designed to stimulate learning at home and at school. Initial content was made available in January 2006; however, BBC Jam was suspended on 20 March 2007 due to allegations made to the European Commission that it was damaging the interests of the commercial sector of the industry.In recent years, some major on-line companies and politicians have complained that BBC Online receives too much funding from the television licence, meaning that other websites are unable to compete with the vast amount of advertising-free on-line content available on BBC Online. Some have proposed that the amount of licence fee money spent on BBC Online should be reduced-either being replaced with funding from advertisements or subscriptions, or a reduction in the amount of content available on the site. In response to this the BBC carried out an investigation, and has now set in motion a plan to change the way it provides its online services. BBC Online will now attempt to fill in gaps in the market, and will guide users to other websites for currently existing market provision. (For example, instead of providing local events information and timetables, users will be guided to outside websites already providing that information.) Part of this plan included the BBC closing some of its websites, and rediverting money to redevelop other parts.On 26 February 2010, The Times claimed that Mark Thompson, Director General of the BBC, proposed that the BBC's web output should be cut by 50%, with online staff numbers and budgets reduced by 25% in a bid to scale back BBC operations and allow commercial rivals more room. On 2 March 2010, the BBC reported that it will cut its website spending by 25% and close BBC 6 Music and Asian Network, as part of Mark Thompson's plans to make "a smaller, fitter BBC for the digital age".BBC Red Button is the brand name for the BBC's interactive digital television services, which are available through Freeview (digital terrestrial), as well as Freesat, Sky (satellite), and Virgin Media (cable). Unlike Ceefax, the service's analogue counterpart, BBC Red Button is able to display full-colour graphics, photographs, and video, as well as programmes and can be accessed from any BBC channel. The service carries News, Weather and Sport 24 hours a day, but also provides extra features related to programmes specific at that time. Examples include viewers to play along at home to gameshows, to give, voice and vote on opinions to issues, as used alongside programmes such as Question Time. At some points in the year, when multiple sporting events occur, some coverage of less mainstream sports or games are frequently placed on the Red Button for viewers to watch. Frequently, other features are added unrelated to programmes being broadcast at that time, such as the broadcast of the Doctor Who animated episode Dreamland in November 2009.The BBC employs staff orchestras, a choir, and supports two amateur choruses, based in BBC venues across the UK; the BBC Symphony Orchestra, the BBC Singers, BBC Symphony Chorus and BBC Big Band based in London, the BBC Scottish Symphony Orchestra in Glasgow, the BBC Philharmonic in Manchester, the BBC Concert Orchestra based in Watford and the BBC National Orchestra of Wales in Cardiff. It also buys a selected number of broadcasts from the Ulster Orchestra in Belfast. Many famous musicians of every genre have played at the BBC, such as The Beatles (The Beatles Live at the BBC is one of their many albums). The BBC is also responsible for the United Kingdom coverage of the Eurovision Song Contest, a show with which the broadcaster has been associated for over 50 years. The BBC also operates the division of BBC Audiobooks sometimes found in association with Chivers Audiobooks.The BBC operates other ventures in addition to their broadcasting arm. In addition to broadcasting output on television and radio, some programmes are also displayed on the BBC Big Screens located in several central-city locations. The BBC and the Foreign and Commonwealth Office also jointly run BBC Monitoring, which monitors radio, television, the press and the internet worldwide. The BBC also developed several computers throughout the 1980s, most notably the BBC Micro, which ran alongside the corporation's educational aims and programming.In 1951, in conjunction with Oxford University Press the BBC published The BBC Hymn Book which was intended to be used by radio listeners to follow hymns being broadcast. The book was published both with and without music, the music edition being entitled The BBC Hymn Book with Music. The book contained 542 popular hymns.The BBC provided the world's first teletext service called Ceefax (near-homonymous with "See Facts") on 23 September 1974 until 23 October 2012 on the BBC 1 analogue channel then later on BBC 2. It showed informational pages such as News, Sport and the Weather. on New Year's Eve in 1974, competition from ITV's Oracle tried to compete with Ceefax. Oracle closed on New Year's Eve, 1992. During its lifetime it attracted millions of viewers, right up to 2012, prior to the digital switchover in the United Kingdom. It ceased transmission at 23:32:19 BST on 23 October 2012 after 38 years. Since then, the BBC's Red Button Service has provided a digital-like information system that replaced Ceefax.Britflix is an upcoming online video streaming service by the BBC.BBC Worldwide Limited is the wholly owned commercial subsidiary of the BBC, responsible for the commercial exploitation of BBC programmes and other properties, including a number of television stations throughout the world. It was formed following the restructuring of its predecessor, BBC Enterprises, in 1995.The company owns and administers a number of commercial stations around the world operating in a number of territories and on a number of different platforms. The channel BBC Entertainment shows current and archive entertainment programming to viewers in Europe, Africa, Asia and the Middle East, with the BBC Worldwide channels BBC America and BBC Canada (Joint venture with Corus Entertainment) showing similar programming in the North America region and BBC UKTV in the Australasia region. The company also airs two channels aimed at children, an international CBeebies channel and BBC Kids, a joint venture with Knowledge Network Corporation, which airs programmes under the CBeebies and BBC K brands. The company also runs the channels BBC Knowledge, broadcasting factual and learning programmes, and BBC Lifestyle, broadcasting programmes based on themes of Food, Style and Wellbeing. In addition to this, BBC Worldwide runs an international version of the channel BBC HD, and provides HD simulcasts of the channels BBC Knowledge and BBC America.BBC Worldwide also distributes the 24-hour international news channel BBC World News. The station is separate from BBC Worldwide to maintain the station's neutral point of view, but is distributed by BBC Worldwide. The channel itself is the oldest surviving entity of its kind, and has 50 foreign news bureaus and correspondents in nearly all countries in the world. As officially surveyed it is available to more than 294 million households, significantly more than CNN's estimated 200 million.  In addition to these international channels, BBC Worldwide also owns, together with Scripps Networks Interactive, the UKTV network of ten channels. These channels contain BBC archive programming to be rebroadcast on their respective channels: Alibi, crime dramas; Drama, drama, launched in 2013; Dave (slogan: "The Home of Witty Banter"); Eden, nature; Gold, comedy; Good Food, cookery; Home, home and garden; Really, female programming; Watch, entertainment; and Yesterday, history programming.In addition to these channels, many BBC programmes are sold via BBC Worldwide to foreign television stations with comedy, documentaries and historical drama productions being the most popular. In addition, BBC television news appears nightly on many Public Broadcasting Service stations in the United States, as do reruns of BBC programmes such as EastEnders, and in New Zealand on TVNZ 1.In addition to programming, BBC Worldwide produces material to accompany programmes. The company maintained the publishing arm of the BBC, BBC Magazines, which published the Radio Times as well as a number of magazines that support BBC programming such as BBC Top Gear, BBC Good Food, BBC Sky at Night, BBC History, BBC Wildlife and BBC Music. BBC Magazines was sold to Exponent Private Equity in 2011, which merged it with Origin Publishing (previously owned by BBC Worldwide between 2004 and 2006) to form Immediate Media Company.BBC Worldwide also publishes books, to accompany programmes such as Doctor Who under the BBC Books brand, a publishing imprint majority owned by Random House. Soundtrack albums, talking books and sections of radio broadcasts are also sold under the brand BBC Records, with DVDs also being sold and licensed in large quantities to consumers both in the UK and abroad under the 2 Entertain brand. Archive programming and classical music recordings are sold under the brand BBC Legends.Until the development, popularisation, and domination of television, radio was the broadcast medium upon which people in the United Kingdom relied. It "reached into every home in the land, and simultaneously united the nation, an important factor during the Second World War". The BBC introduced the world's first "high-definition" 405-line television service in 1936. It suspended its television service during the Second World War and until 1946, but remained the only television broadcaster in the UK until 1955. "The BBC's monopoly was broken in 1955, with the introduction of Independent Television (ITV)". This heralded the transformation of television into a popular and dominant medium. Nevertheless, "throughout the 1950s radio still remained the dominant source of broadcast comedy". Further, the BBC was the only legal radio broadcaster until 1968 (when URY obtained their first licence).Despite the advent of commercial television and radio, the BBC has remained one of the main elements in British popular culture through its obligation to produce TV and radio programmes for mass audiences. However, the arrival of BBC2 allowed the BBC also to make programmes for minority interests in drama, documentaries, current affairs, entertainment, and sport. Examples cited include the television series Civilisation, Doctor Who, I, Claudius, Monty Python's Flying Circus, Pot Black, and Tonight, but other examples can be given in each of these fields as shown by the BBC's entries in the British Film Institute's 2000 list of the 100 Greatest British Television Programmes. The export of BBC programmes both through services like the BBC World Service and BBC World News, as well as through the channels operated by BBC Worldwide, means that audiences can consume BBC productions worldwide.The term "BBC English" was used as an alternative name for Received Pronunciation, and the English Pronouncing Dictionary uses the term "BBC Pronunciation" to label its recommendations. However, the BBC itself now makes more use of regional accents in order to reflect the diversity of the UK, while continuing to expect clarity and fluency of its presenters. From its "starchy" beginnings, the BBC has also become more inclusive, and now attempts to accommodate the interests of all strata of society and all minorities, because they all pay the licence fee.Competition from Independent Television, Channel 4, Sky, and other broadcast-television stations has lessened the BBC's influence, but its public broadcasting remains a major influence on British popular culture.Older domestic UK audiences often refer to the BBC as "the Beeb", a nickname originally coined by Peter Sellers on The Goon Show in the 1950s, when he referred to the "Beeb Beeb Ceeb". It was then borrowed, shortened and popularised by Kenny Everett. Another nickname, now less commonly used, is "Auntie", said to originate from the old-fashioned "Auntie knows best" attitude, or the idea of aunties and uncles who are present in the background of one's life (but possibly a reference to the "aunties" and "uncles" who presented children's programmes in the early days) in the days when John Reith, the BBC's first director general, was in charge. The two nicknames have also been used together as "Auntie Beeb".The BBC has faced various accusations regarding many topics: the Iraq war, politics, ethics and religion, as well as funding and staffing. It also has been involved in numerous controversies because of its different, sometimes very controversial coverage of specific news stories and programming. In October 2014, the BBC Trust issued the "BBC complaints framework", outlining complaints and appeals procedures. However, the regulatory oversight of the BBC may be transferred to OFCOM. The British "House of Commons Select Committee on Culture Media and Sport" recommended in its report "The Future of the BBC", that OFCOM should become the final arbiter of complaints made about the BBC.Accusations of a bias against the government and the Conservative Party were often made against the Corporation by members of Margaret Thatcher's 1980s Conservative government. BBC presenter Andrew Marr has said that "The BBC is not impartial or neutral. It has a liberal bias, not so much a party-political bias. It is better expressed as a cultural liberal bias." Conversely, the BBC has been criticised by The Guardian columnist, Owen Jones, who has said that "the truth is the BBC is stacked full of rightwingers." Paul Mason, the former Economics Editor of the BBC's Newsnight programme, has also criticised the BBC as "unionist" in relation to the BBC's coverage of the 2014 Scottish referendum campaign and "neo-liberal". However, Peter Sissons, a main news presenter at the BBC from 1989-2009, who from 1964-1989 worked as a journalist and then senior presenter at ITN, latterly at Channel 4 News, says "At the core of the BBC, in its very DNA, is a way of thinking that is firmly of the Left". The BBC has also been characterised as a pro-monarchist institution. The BBC was also accused of propaganda by journalist and author Toby Young, due to what he believed to be an anti-Brexit approach including a whole day of live programming on migration.The BBC World Service was involved in the Kyrgyz revolution in April 2010. One of the news presenters and a producer of the BBC World Service language, was revealed to have participated in the opposition movement at the time, with the goal to overthrow the Kyrgyzstan government led by president Kurmanbek Bakiyev using BBC resources. The BBC producer resigned from his post in 2010 once the news of his participation in the revolution became public. The BBC World Service neither confirmed nor denied this story, nor did the service issue a statement about this story. BBC documentary made by Justin Rowlatt, 'One World: Killing for Conservation' questions India s aggressive protection methods at Kaziranga National park, Assam. The documentary claimed that forest guards in this national park had been given authority to shoot and kill anyone, who would prove to be a threat to rhinos. The documentary was criticized by the Union environment for being "grossly erroneous". Following this, the National Conservation Authority (NTCA) in India imposed a ban on BBC and its journalist Justin Rowlatt for five years."""

###########################------Multiprocessing Manager Definition-----###########################
manager = Manager()

parsey_lock = manager.Lock()
parse_wiktionary_lock = manager.Lock()
shared_sentence_graph_count = manager.Value('L', 0)
shared_sentence_graphs_list = manager.list()

shared_basis_sentence_graphs_list = manager.list()
###################################################################################################

def print_reduction_statistics(
        sentence, sentence_graph, reduced_sentence_graph):
    print("Sentence: %s" % sentence)
    print("Vertices in original graph: %d" 
        % len([x for x in sentence_graph.get_vertices()]))
    print("Vertices in reduced graph: %d" 
        % len([x for x in reduced_sentence_graph.get_vertices()]))


def combine_sentence_graphs(sentence_graphs, directed=True):
    body_of_text = '. '.join([x.get_sentence() for x in sentence_graphs])
    combined_sentence_graph = SentenceGraph(body_of_text, directed)
    
    print("Iterating over %d sentence graphs" % len(sentence_graphs))
    sentence_graph_count = 0
    prev_sentence_last_word_vertex = None
    for sentence_graph in sentence_graphs:

        # TODO: Make this actually be the last word of the sentence
        # Right now it is just whatever vertex is returned last by the iterator, which is arbitrary
        # with respect to the original sentence ordering
        # In general sentence order should be preserved in sentence graphs as well as parse tree info
        last_word_in_sentence = None
        for vertex in sentence_graph.get_vertices_iterator():
            vertex_word_pos_tuple = sentence_graph.get_word_pos_tuple(vertex)
            if not combined_sentence_graph.contains(vertex_word_pos_tuple[0], vertex_word_pos_tuple[1]):
                last_word_in_sentence = combined_sentence_graph.add_vertex(vertex_word_pos_tuple[0], vertex_word_pos_tuple[1])
            else:
                last_word_in_sentence = combined_sentence_graph.get_vertex(vertex_word_pos_tuple[0], vertex_word_pos_tuple[1])

        if prev_sentence_last_word_vertex is not None:
            combined_sentence_graph.add_inter_sentence_edge(prev_sentence_last_word_vertex, last_word_in_sentence)
        prev_sentence_last_word_vertex = last_word_in_sentence

        sentence_edge_properties = sentence_graph.get_sentence_edge_properties()
        definition_edge_properties = sentence_graph.get_definition_edge_properties()
        inter_sentence_edge_properties = sentence_graph.get_inter_sentence_edge_properties()
        print("Iterating over %d edges" % len(sentence_graph.get_edges()))
        edge_count = 0
        for edge in sentence_graph.get_edges_iterator():
            source_vertex_pos_tuple = sentence_graph.get_word_pos_tuple(edge.source())
            target_vertex_pos_tuple = sentence_graph.get_word_pos_tuple(edge.target())
            if sentence_edge_properties[edge] != '':
                print("Adding sentence edge from words: ((%s, %s) (%s, %s))"
                    % (source_vertex_pos_tuple[0], 
                    source_vertex_pos_tuple[1], 
                    target_vertex_pos_tuple[0], 
                    target_vertex_pos_tuple[1]))
                combined_sentence_graph.add_sentence_edge_from_words(
                    source_vertex_pos_tuple[0], 
                    source_vertex_pos_tuple[1], 
                    target_vertex_pos_tuple[0], 
                    target_vertex_pos_tuple[1])
            elif definition_edge_properties != '':
                print("Adding definition edge from words: ((%s, %s) (%s, %s))"
                    % (source_vertex_pos_tuple[0], 
                    source_vertex_pos_tuple[1], 
                    target_vertex_pos_tuple[0], 
                    target_vertex_pos_tuple[1]))
                combined_sentence_graph.add_definition_edge_from_words(
                    source_vertex_pos_tuple[0], 
                    source_vertex_pos_tuple[1], 
                    target_vertex_pos_tuple[0], 
                    target_vertex_pos_tuple[1])
            elif inter_sentence_edge_properties[edge] != '':
                print("Adding inter sentence edge from words: ((%s, %s) (%s, %s))"
                    % (source_vertex_pos_tuple[0], 
                    source_vertex_pos_tuple[1], 
                    target_vertex_pos_tuple[0], 
                    target_vertex_pos_tuple[1]))
                combined_sentence_graph.add_inter_sentence_edge_from_words(
                    source_vertex_pos_tuple[0], 
                    source_vertex_pos_tuple[1], 
                    target_vertex_pos_tuple[0], 
                    target_vertex_pos_tuple[1])
            else:
                print("Error, edge %s not found in definition or sentence properties" % edge)
            edge_count += 1
            print("Edge count: %d" % edge_count)

        sentence_graph_count += 1
        print("Sentence graph count: %d" % sentence_graph_count)
    print("Finished combining %d sentence graphs!" % len(sentence_graphs))
    return combined_sentence_graph

def sentence_graph_creation_func(sentence):
    global parsey_lock
    global parse_wiktionary_lock
    global shared_sentence_graphs_list
    global shared_sentence_graph_count

    sentence = sentence.replace("\\n", "")

    print("Creating sentence graph for sentence: ||%s||" % sentence)
    sys.stdout.flush()
    depth = 2
    directed = True
    use_sentence_graph_cache = False
    use_definition_cache = True

    loaded_from_file = False
    if use_sentence_graph_cache:
        loaded_from_file = True
        sentence = sentence.strip()
        sentence_graph = load_sentence_graph_from_file(
            sentence_graph_file_path_from_sentence("depth=" + str(depth) + "--" + sentence),
            sentence)

    if not use_sentence_graph_cache or sentence_graph is None:
        sentence_graph =\
            build_deep_sentence_graph(
                sentence, 
                WiktionaryClient(parse_wiktionary_lock), 
                directed=directed, 
                depth=depth,
                use_definition_cache=use_definition_cache,
                parsey_lock=parsey_lock)
        loaded_from_file = False

    shared_sentence_graphs_list.append(sentence_graph)
    shared_sentence_graph_count.set(shared_sentence_graph_count.get() + 1)

    if not use_sentence_graph_cache or not loaded_from_file:
        # Save sentence graphs
        save_sentence_graph_to_file(
            sentence_graph, 
            sentence_graph_file_path_from_sentence("depth=" + str(depth) + "--" + sentence))

    """
    # Apparently this causes a race. Don't uncomment this.
    print("Drawing sentence graph!")
    sys.stdout.flush()
    sentence_graph_draw(
        sentence_graph,
        sentence,
        output_folder_name="sentence-graphs-visualization/",
        output_file_name=sentence.strip().replace(" ", "-"))
    print("Drew sentence graph!")
    sys.stdout.flush()
    
    print("Drawing sentence graph.......")
    sys.stdout.flush()
    sentence_graph_draw(
        sentence_graph,
        sentence,
        output_folder_name="sentence-graphs-visualization/",
        output_file_name=sentence.strip().replace(" ", "-"))
    print("Drew sentence graph!")
    sys.stdout.flush()

    print("Running kcore decomposition")
    graph = sentence_graph.get_graph()
    kcore_property_map = topology.kcore_decomposition(graph)
    sys.stdout.flush()
    print("Drawing kcore decomposition.......")
    graph_draw(
        graph, 
        output_size=(30000, 30000), 
        output=sentence.strip().replace(" ", "-") + "--kcore.png",
        vertex_text=sentence_graph.get_word_vertex_properties(), 
        vertex_size=25,
        vertex_font_size=25,
        vertex_fill_color=kcore,
        edge_color=sentence_graph.get_color_edge_properties())
    print("Drew kcore decomposition!")
    #"""

    return sentence_graph

def sentence_graph_to_dissimilarity_vector_func(sentence_graph):
    global shared_basis_sentence_graphs_list

    print("Running on sentence_graph: %s" % sentence_graph.get_sentence())
    print("shared_basis_sentences: %s" % '\n'.join([x.get_sentence() for x in shared_basis_sentence_graphs_list]))
    dissimilarity_vector = sentence_graph_dissimilarity_embedding(sentence_graph, shared_basis_sentence_graphs_list)
    print("For sentence: %s\nDissimilarity vector: %s\n" % (sentence_graph.get_sentence(), dissimilarity_vector))
    return dissimilarity_vector

def sentence_graphs_to_dissimilarity_vectors_func(sentence_graphs, basis_sentence_graphs):
    print("Dissimilarity vector sentences: ")
    for basis_sentence_graph in basis_sentence_graphs:
        print("%s" % basis_sentence_graph.get_sentence())
    dissimilarity_vectors = list()
    for sentence_graph in sentence_graphs:
        dissimilarity_vector = sentence_graph_dissimilarity_embedding(sentence_graph, basis_sentence_graphs)
        dissimilarity_vectors.append(dissimilarity_vector)
        print("For sentence: %s\nDissimilarity vector: %s\n" % (sentence_graph.get_sentence(), dissimilarity_vector))
    return dissimilarity_vectors    

def test():
    """
    print("Loading sentence graph from file.....")
    sentence_graph = load_sentence_graph_from_file("sentence-graphs-storage/Minimum_description_length.gt", "Minimum Description Length")
    print("Finished loading sentence graph from file!")
    print("Drawing sentence graph.......")
    sentence_graph_draw(
            sentence_graph, 
            "Minimum desription length wikipedia page",
            output_file_name="Minimum-description-length-wiki-page")
    print("Done.")
    return 
    #"""
    global DEBUG_restart_sentence_index
    global shared_basis_sentence_graphs_list

    clear_wiktionary_file_locks()
    
    sentences = BBC_ARTICLE.split('.')
    sentences = filter(lambda x: x.strip() != '', sentences)

    # Multiprocess runner
    # The Pool must be instantiated after the sentence_graph_creation_func
    # so that the child processes have access to the sentence_graph_creation_func.
    # This is because the process forks when Pool() is called and if sentence_graph_creation_func
    # has not been defined yet the children will not have a reference to it
    pool = Pool()

    # Wikipedia random access + graph edit distance
    #"""
    page_limit = 50
    dimensions = 3
    all_sentence_graphs = list()
    #wikipedia_articles = scrape_wikipedia(randomize=True, page_limit=page_limit)
    wikipedia_urls = [
        "https://en.wikipedia.org/wiki/Minimum_description_length",
        #"https://en.wikipedia.org/wiki/Quantum_mechanics",
        #"https://en.wikipedia.org/wiki/Queen_Victoria",
        #"https://en.wikipedia.org/wiki/Reddit",
        #"https://en.wikipedia.org/wiki/Snoop_Dogg",
        #"https://en.wikipedia.org/wiki/Goldman_Sachs",
        #"https://en.wikipedia.org/wiki/Virginia",
        #"https://en.wikipedia.org/wiki/Germany",
        #"https://en.wikipedia.org/wiki/Mars",
        #"https://en.wikipedia.org/wiki/NASA",
    ]
    wikipedia_articles = scrape_wikipedia_articles(wikipedia_urls)
    for wikipedia_article in wikipedia_articles:

        print("Wikipedia_article['body']: %s\n" % wikipedia_article["body"])
        print("-------------------------------END WIKIPEDIA ARTICLE BODY---------------------------------")

        sentences = wikipedia_article["body"].split('.')
        sentences = filter(lambda x: not x.isspace(), sentences)
        if len(sentences) <= dimensions:
            continue

        #wiki_page_sentence_graphs = pool.map(sentence_graph_creation_func, sentences, 1)
        wiki_page_sentence_graphs = list()
        for sentence in sentences:
            wiki_page_sentence_graphs.append(sentence_graph_creation_func(sentence))
        wikipedia_article["sentence_graphs"] = wiki_page_sentence_graphs
        all_sentence_graphs += wiki_page_sentence_graphs

        #"""
        for wiki_page_sentence_graph, wiki_page_sentence in zip(wiki_page_sentence_graphs, sentences):
            print("Drawing sentence graph.......")
            sys.stdout.flush()
            sentence_graph_draw(
                wiki_page_sentence_graph,
                wiki_page_sentence,
                output_folder_name="sentence-graphs-visualization/",
                output_file_name=wiki_page_sentence.strip().replace(" ", "-"))
            print("Drew sentence graph!")
            sys.stdout.flush()

            """
            print("Running kcore decomposition")
            graph = wiki_page_sentence_graph.get_graph()
            kcore_property_map = topology.kcore_decomposition(graph)
            sys.stdout.flush()
            print("Drawing kcore decomposition.......")
            graph_draw(
                graph, 
                output_size=(30000, 30000), 
                output=wiki_page_sentence.strip().replace(" ", "-") + "--kcore.png",
                vertex_text=wiki_page_sentence_graph.get_word_vertex_properties(), 
                vertex_size=25,
                vertex_font_size=25,
                vertex_fill_color=kcore,
                edge_color=wiki_page_sentence_graph.get_color_edge_properties())
            print("Drew kcore decomposition!")
            #"""
        #"""
        print("Processed %s sentences" % str(shared_sentence_graph_count))
        shared_sentence_graph_count.set(0)
        print("\n\n\n")

        """
        # Combine sentence graphs
        combined_sentence_graph = combine_sentence_graphs(all_sentence_graphs)

        print("Saving combined sentence graph to file.......")
        sys.stdout.flush()
        save_sentence_graph_to_file(
                combined_sentence_graph, 
                sentence_graph_file_path_from_sentence("Minimum_description_length"))
        print("Saved sentence graph to file!")
        sys.stdout.flush()

        print("Drawing combined sentence graph.......")
        sys.stdout.flush()
        sentence_graph_draw(
            combined_sentence_graph, 
            "Minimum desription length wikipedia page--truncated-debugging",
            output_file_name="Minimum-description-length-wiki-page")
        print("Drew sentence graph!")
        sys.stdout.flush()
        """
    sys.stdout.flush()
    print("Created %d sentence graphs total" % len(all_sentence_graphs))

    """
    print("Selecting prototype graphs.......")
    basis_sentence_graphs, basis_sentence_graph_indices = select_prototype_graphs(all_sentence_graphs, dimensions)
    shared_basis_sentence_graphs_list.extend(basis_sentence_graphs)
    # Remove the sentence graphs that are being used as a basis.
    # Sort the indices in reverse so we remove from the highest indices down to the lowest
    # thus preserving the validity of the remaining indices
    for index in sorted(basis_sentence_graph_indices, reverse=True):
        all_sentence_graphs.pop(index)
    print("Prototype graphs selected!")

    print("Computing dissimilarity vectors for %d sentence graphs using %d prototype sentence graphs" 
          % (len(all_sentence_graphs), len(basis_sentence_graphs)))
    sys.stdout.flush()
    dissimilarity_vectors_list = pool.map(sentence_graph_to_dissimilarity_vector_func, all_sentence_graphs, 1)

    print("\n Basis sentences: %s" % '\n'.join([sentence_graph.get_sentence() for sentence_graph in basis_sentence_graphs]))
    plot_3d_vectors(dissimilarity_vectors_list, labels=sentences, show_figure=True)
    #"""

    # Corex testing
    """
    sentence_graphs = pool.map(sentence_graph_creation_func, sentences, 1)

    wikipedia_article["sentence_graphs"] = sentence_graphs

    print("Processed %s sentences" % str(shared_sentence_graph_count))

    for sentence_graph in sentence_graphs:
        save_sentence_graph_to_file(
            sentence_graph, 
            sentence_graph_file_path_from_sentence(sentence_graph.get_sentence()))

    corex = Corex()
    corex.initialize_parameters(
        sentence_graphs_to_vectors(sentence_graphs))
    """

    pool.close()

def pairwise_sentence_similarity_on_sick_item(sick_item):
    sentence_graph1 = sentence_graph_creation_func(sick_item.sentence1)
    sentence_graph2 = sentence_graph_creation_func(sick_item.sentence2)

    """
    # Filter out sentence_edges
    sentence_graph1.set_sentence_edge_filter(inverted=True)
    sentence_graph2.set_sentence_edge_filter(inverted=True)
    #"""

    """
    # Filter out parsed_dependency_edges
    sentence_graph1.set_parsed_dependency_edge_filter(inverted=True)
    sentence_graph2.set_parsed_dependency_edge_filter(inverted=True)
    #"""

    """
    cProfile.run("sentence_graphs_to_dissimilarity_vectors_func("\
        "[sentence_graph1],"\
        "prototype_sentence_graphs)")
    #"""
    graph_edit_distance = approximate_sentence_graph_edit_distance(sentence_graph1, sentence_graph2)
    # Convert distance to similarity
    similarity_between_sentence_graphs = 1 / graph_edit_distance if graph_edit_distance != 0 else 1
    # Map the similarity scores to the range [0, 5]
    similarity_between_sentence_graphs = 10 * (similarity_between_sentence_graphs / (np.absolute(similarity_between_sentence_graphs) + 1))

    # Compute the graph tool similarity score
    graph_tool_similarity_score = topology.similarity(sentence_graph1.get_graph(), sentence_graph2.get_graph())
    #"""

    print("For sentence1: %s\n and sentence2:%s\n"
        "With a distance of:\n%s\n"
        "A calculated similarity score of:\n%s\n"
        "The topology similarity score is:\n%s\n"
        "The expected output (1-5) is:%s\n"
        "The sentence pair id is:%s\n"
        % (sick_item.sentence1, 
        sick_item.sentence2, 
        graph_edit_distance,
        similarity_between_sentence_graphs,
        graph_tool_similarity_score,
        sick_item.similarity_score,
        sick_item.sentence_pair_id))
    return (sentence_graph1, 
        sentence_graph2, 
        graph_edit_distance,
        similarity_between_sentence_graphs,
        graph_tool_similarity_score,
        sick_item.similarity_score,
        sick_item.sentence_pair_id)

def sick_dataset_test():
    pool = Pool()

    sick_root_path = "../../sentence-similarity-datasets/sick/sick2014"
    sick_dataset = load_sick_dataset(sick_root_path, "SICK_trial.txt")
    result_tuples = pool.map(pairwise_sentence_similarity_on_sick_item, sick_dataset)
    #result_tuples = list()
    #for sick_item in sick_dataset:
    #    result_tuples.append(pairwise_sentence_similarity_on_sick_item(sick_item))

    print("Finished calculating distances!")
    print("Drawing sentence graphs for debugging.....")
    sys.stdout.flush()
    for result_tuple in result_tuples:
        print("Drawing sentence graph.......")
        sys.stdout.flush()
        sentence_graph_draw(
            result_tuple[0],
            result_tuple[0].get_sentence(),
            output_folder_name="sentence-graphs-visualization/",
            output_file_name=result_tuple[0].get_sentence().strip().replace(" ", "-"))
        print("Drew sentence graph!")
        sys.stdout.flush()

        print("Drawing sentence graph.......")
        sys.stdout.flush()
        sentence_graph_draw(
            result_tuple[1],
            result_tuple[1].get_sentence(),
            output_folder_name="sentence-graphs-visualization/",
            output_file_name=result_tuple[1].get_sentence().strip().replace(" ", "-"))
        print("Drew sentence graph!")
        sys.stdout.flush()
    print("Finished drawing sentence graphs!")

    pool.close()


def pairwise_sentence_similarity_on_sts_dataset(sts_dataset_name):
    sts_root_path = "../../sentence-similarity-datasets/sts-2014/sts-en-trial-2014"
    print("Running on dataset named: %s" % sts_dataset_name)
    sts_dataset = load_sts_dataset(sts_root_path, sts_dataset_name)
    for sts_item in sts_dataset:
        sentence_graph1 = sentence_graph_creation_func(sts_item.sentence1)
        sentence_graph2 = sentence_graph_creation_func(sts_item.sentence2)

        """
        # Filter out sentence_edges
        sentence_graph1.set_sentence_edge_filter(inverted=True)
        sentence_graph2.set_sentence_edge_filter(inverted=True)
        #"""

        """
        # Filter out parsed_dependency_edges
        sentence_graph1.set_parsed_dependency_edge_filter(inverted=True)
        sentence_graph2.set_parsed_dependency_edge_filter(inverted=True)
        #"""

        """
        cProfile.run("sentence_graphs_to_dissimilarity_vectors_func("\
            "[sentence_graph1],"\
            "prototype_sentence_graphs)")
        #"""
        graph_edit_distance = approximate_sentence_graph_edit_distance(sentence_graph1, sentence_graph2)
        # Convert distance to similarity
        similarity_between_sentence_graphs = 1 / graph_edit_distance
        # Map the similarity scores to the range [0, 5]
        similarity_between_sentence_graphs = 5 * (similarity_between_sentence_graphs / (np.absolute(similarity_between_sentence_graphs) + 1))

        # Compute the graph tool similarity score
        graph_tool_similarity_score = topology.similarity(sentence_graph1.get_graph(), sentence_graph2.get_graph())
        #"""

        print("From dataset: %s\n"
            "For sentence1: %s\n and sentence2:%s\n"
            "With a distance of:\n%s\n"
            "A calculated similarity score of:\n%s\n"
            "The topology similarity score is:\n%s\n"
            "The expected output (1-5) is:%s\n"
            "The gold standard (1-5) is:%s\n"
            % (sts_dataset_name,
            sts_item.sentence1, 
            sts_item.sentence2, 
            graph_edit_distance,
            similarity_between_sentence_graphs,
            graph_tool_similarity_score,
            sts_item.output_similarity,
            sts_item.gold_standard_score))
    return (sentence_graph1, 
        sentence_graph2, 
        graph_edit_distance,
        similarity_between_sentence_graphs,
        graph_tool_similarity_score,
        sts_item.output_similarity,
        sts_item.gold_standard_score)

def sentence_similarity_on_sts_dataset(sts_dataset_name):
    sts_root_path = "../../sentence-similarity-datasets/sts-2014/sts-en-trial-2014"
    print("Running on dataset named: %s" % sts_dataset_name)
    sts_dataset = load_sts_dataset(sts_root_path, sts_dataset_name)
    for sts_item in sts_dataset:
        sentence_graph1 = sentence_graph_creation_func(sts_item.sentence1)
        sentence_graph2 = sentence_graph_creation_func(sts_item.sentence2)

        """
        cProfile.run("sentence_graphs_to_dissimilarity_vectors_func("\
            "[sentence_graph1],"\
            "prototype_sentence_graphs)")
        #"""
        dissimilarity_vectors = sentence_graphs_to_dissimilarity_vectors_func(
            [sentence_graph1, sentence_graph2], 
            prototype_sentence_graphs)
        distance_between_vectors = linalg.norm(np.array(dissimilarity_vectors[0]) - np.array(dissimilarity_vectors[1]))
        # Convert distance to similarity
        similarity_between_sentence_graphs = 1 / distance_between_vectors
        # Map the similarity scores to the range [0, 5]
        similarity_between_sentence_graphs = 5 * (similarity_between_sentence_graphs / (np.absolute(similarity_between_sentence_graphs) + 1))

        # Compute the graph tool similarity score
        graph_tool_similarity_score = topology.similarity(sentence_graph1.get_graph(), sentence_graph2.get_graph())
        #"""

        print("For sentence1: %s\n and sentence2:%s\n"
            "the dissimilarity vectors are:\n%s\nand\n%s\n"
            "With a distance of:\n%s\n"
            "A calculated similarity score of:\n%s\n"
            "The topology similarity score is:\n%s\n"
            "The expected output (1-5) is:%s\n"
            "The gold standard (1-5) is:%s\n"
            % (sts_item.sentence1, 
            sts_item.sentence2, 
            dissimilarity_vectors[0], 
            dissimilarity_vectors[1], 
            distance_between_vectors,
            similarity_between_sentence_graphs,
            graph_tool_similarity_score,
            sts_item.output_similarity,
            sts_item.gold_standard_score))
    return (sentence_graph1, 
        sentence_graph2, 
        dissimilarity_vectors[0], 
        dissimilarity_vectors[1],
        distance_between_vectors,
        similarity_between_sentence_graphs,
        graph_tool_similarity_score,
        sts_item.output_similarity,
        sts_item.gold_standard_score)

def sts_dataset_test():
    prototype_sentences = [
        "Jack Johnson said the sky is flurescent yellow",
        "The intrinsic complexity of this sentence is inherent once you read it twice",
        "Curiosity is the greatest invention that mankind has ever produced",
        "America is surely the greatest country that has ever existed",
        "It will be wonderful if these sentences actually produce something useful"
    ]
    prototype_sentence_graphs = list()
    for prototype_sentence in prototype_sentences:
        prototype_sentence_graphs.append(
            sentence_graph_creation_func(prototype_sentence))

    pool = Pool()

    #"""
    # Sts testing over all datasets
    sts_root_path = "../../sentence-similarity-datasets/sts-2014/sts-en-trial-2014"
    #result_tuples = pool.map(sentence_similarity_on_sts_dataset, get_sts_dataset_names())
    result_tuples = pool.map(pairwise_sentence_similarity_on_sts_dataset, get_sts_dataset_names())
    print("Finished calculating distances!")
    print("Drawing sentence graphs for debugging.....")
    sys.stdout.flush()
    for result_tuple in result_tuples:
        print("Drawing sentence graph.......")
        sys.stdout.flush()
        sentence_graph_draw(
            result_tuple[0],
            result_tuple[0].get_sentence(),
            output_folder_name="sentence-graphs-visualization/",
            output_file_name=result_tuple[0].get_sentence().strip().replace(" ", "-"))
        print("Drew sentence graph!")
        sys.stdout.flush()

        print("Drawing sentence graph.......")
        sys.stdout.flush()
        sentence_graph_draw(
            result_tuple[1],
            result_tuple[1].get_sentence(),
            output_folder_name="sentence-graphs-visualization/",
            output_file_name=result_tuple[1].get_sentence().strip().replace(" ", "-"))
        print("Drew sentence graph!")
        sys.stdout.flush()
    print("Finished drawing sentence graphs!")
    #"""

    """
    # Sts testing over first dataset only
    for sts_dataset_name in [get_sts_dataset_names()[0]]:

        print("Running on dataset named: %s" % sts_dataset_name)
        sts_dataset = load_sts_dataset(sts_root_path, sts_dataset_name)
        for sts_item in sts_dataset:
            sentence_graph1 = sentence_graph_creation_func(sts_item.sentence1)
            sentence_graph2 = sentence_graph_creation_func(sts_item.sentence2)

            #cProfile.run("sentence_graphs_to_dissimilarity_vectors_func("\
            #    "[sentence_graph1],"\
            #    "prototype_sentence_graphs)")
            
            dissimilarity_vectors = sentence_graphs_to_dissimilarity_vectors_func(
                [sentence_graph1, sentence_graph2], 
                prototype_sentence_graphs)
            distance_between_vectors = linalg.norm(np.array(dissimilarity_vectors[0]) - np.array(dissimilarity_vectors[1]))
            distance_between_vectors = 5 * (distance_between_vectors / (np.absolute(distance_between_vectors) + 1))
            
            print("For sentence1: %s\n and sentence2:%s\n"
                "the dissimilarity vectors are:\n%s\nand\n%s\n"
                "With a distance of:\n%s\n"
                "The expected output (1-5) is:%s\n"
                "The gold standard (1-5) is:%s\n"
                % (sts_item.sentence1, 
                sts_item.sentence2, 
                dissimilarity_vectors[0], 
                dissimilarity_vectors[1], 
                distance_between_vectors,
                sts_item.output_similarity,
                sts_item.gold_standard_score))
    #"""
    pool.close()

if __name__ == '__main__':
    #test()
    #sts_dataset_test()
    sick_dataset_test()