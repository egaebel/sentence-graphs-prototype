from aylienapiclient import textapi

from graph_tool.all import Graph
from graph_tool.all import graph_draw
from graph_tool.all import load_graph
from graph_tool import topology

from pylocker import Locker

import scrapy

from multiprocessing import cpu_count
from multiprocessing import Lock
from multiprocessing import Manager
from multiprocessing import Pool
import itertools
import json
import os
import os.path
import re
import subprocess
import sys
import time
import types
import uuid

# Use functions from parsey-mcparseface-service
sys.path.insert(1, "../../parsey-mcparseface-service/src/")
from run_parsey import run_parsey
from parse_tree_parser import parse_ascii_tree


DEBUG_restart_sentence_index = 0

BBC_ARTICLE = """The British Broadcasting Corporation (BBC) is a British public service broadcaster. It is headquartered at Broadcasting House in London, is the world's oldest national broadcasting organisation, and is the largest broadcaster in the world by number of employees, with over 20,950 staff in total, of whom 16,672 are in public sector broadcasting; when part-time, flexible and fixed contract staff are included, the total number is 35,402.The BBC is established under a Royal Charter and operates under its Agreement with the Secretary of State for Culture, Media and Sport. Its work is funded principally by an annual television licence fee which is charged to all British households, companies, and organisations using any type of equipment to receive or record live television broadcasts. The fee is set by the British Government, agreed by Parliament, and used to fund the BBC's radio, TV, and online services covering the nations and regions of the UK. Since 1 April 2014, it has also funded the BBC World Service (launched in 1932 as the BBC Empire Service), which broadcasts in 28 languages and provides comprehensive TV, radio, and online services in Arabic, and Persian.Around a quarter of BBC revenues come from its commercial arm BBC Worldwide Ltd, which sells BBC programmes and services internationally and also distributes the BBC's international 24-hour English-language news services BBC World News, and from BBC.com, provided by BBC Global News Ltd.Britain's first live public broadcast from the Marconi factory in Chelmsford took place in June 1920. It was sponsored by the Daily Mail's Lord Northcliffe and featured the famous Australian Soprano Dame Nellie Melba. The Melba broadcast caught the people's imagination and marked a turning point in the British public's attitude to radio. However, this public enthusiasm was not shared in official circles where such broadcasts were held to interfere with important military and civil communications. By late 1920, pressure from these quarters and uneasiness among the staff of the licensing authority, the General Post Office (GPO), was sufficient to lead to a ban on further Chelmsford broadcasts.But by 1922, the GPO had received nearly 100 broadcast licence requests and moved to rescind its ban in the wake of a petition by 63 wireless societies with over 3,000 members. Anxious to avoid the same chaotic expansion experienced in the United States the GPO proposed that it would issue a single broadcasting licence to a company jointly owned by a consortium of leading wireless receiver manufactures, to be known as the British Broadcasting Company Ltd. John Reith, a Scottish Calvinist, was appointed its General Manager in December 1922 a few weeks after the company made its first official broadcast. The company was to be financed by a royalty on the sale of BBC wireless receiving sets from approved manufacturers. To this day, the BBC aims to follow the Reithian directive to "inform, educate and entertain".The financial arrangements soon proved inadequate. Set sales were disappointing as amateurs made their own receivers and listeners bought rival unlicensed sets. By mid-1923, discussions between the GPO and the BBC had become deadlocked and the Postmaster-General commissioned a review of broadcasting by the Sykes Committee. The Committee recommended a short term reorganisation of licence fees with improved enforcement in order to address the BBC's immediate financial distress, and an increased share of the licence revenue split between it and the GPO. This was to be followed by a simple 10 shillings licence fee with no royalty once the wireless manufactures protection expired. The BBC's broadcasting monopoly was made explicit for the duration of its current broadcast licence, as was the prohibition on advertising. The BBC was also banned from presenting news bulletins before 19.00, and required to source all news from external wire services.Mid-1925 found the future of broadcasting under further consideration, this time by the Crawford committee. By now the BBC under Reith's leadership had forged a consensus favouring a continuation of the unified (monopoly) broadcasting service, but more money was still required to finance rapid expansion. Wireless manufacturers were anxious to exit the loss making consortium with Reith keen that the BBC be seen as a public service rather than a commercial enterprise. The recommendations of the Crawford Committee were published in March the following year and were still under consideration by the GPO when the 1926 general strike broke out in May. The strike temporarily interrupted newspaper production and with restrictions on news bulletins waived the BBC suddenly became the primary source of news for the duration of the crisis.The crisis placed the BBC in a delicate position. On one hand Reith was acutely aware that the Government might exercise its right to commandeer the BBC at any time as a mouthpiece of the Government if the BBC were to step out of line, but on the other he was anxious to maintain public trust by appearing to be acting independently. The Government was divided on how to handle the BBC but ended up trusting Reith, whose opposition to the strike mirrored the PM's own. Thus the BBC was granted sufficient leeway to pursue the Government's objectives largely in a manner of its own choosing. The resulting coverage of both striker and government viewpoints impressed millions of listeners who were unaware that the PM had broadcast to the nation from Reith's home, using one of Reith's sound bites inserted at the last moment, or that the BBC had banned broadcasts from the Labour Party and delayed a peace appeal by the Archbishop of Canterbury. Supporters of the strike nicknamed the BBC the BFC for British Falsehood Company. Reith personally announced the end of the strike which he marked by reciting from Blake's "Jerusalem" signifying that England had been saved.While the BBC tends to characterise its coverage of the general strike by emphasising the positive impression created by its balanced coverage of the views of government and strikers, Jean Seaton, Professor of Media History and the Official BBC Historian has characterised the episode as the invention of "modern propaganda in its British form". Reith argued that trust gained by 'authentic impartial news' could then be used. Impartial news was not necessarily an end in itself.The BBC did well out of the crisis, which cemented a national audience for its broadcasting, and it was followed by the Government's acceptance of the recommendation made by the Crawford Committee (1925-26) that the British Broadcasting Company be replaced by a non-commercial, Crown-chartered organisation: the British Broadcasting Corporation.The British Broadcasting Corporation came into existence on 1 January 1927, and Reith - newly knighted - was appointed its first Director General. To represent its purpose and (stated) values, the new corporation adopted the coat of arms, including the motto "Nation shall speak peace unto Nation".British radio audiences had little choice apart from the upscale programming of the BBC. Reith, an intensely moralistic executive, was in full charge. His goal was to broadcast, "All that is best in every department of human knowledge, endeavour and achievement.... The preservation of a high moral tone is obviously of paramount importance." Reith succeeded in building a high wall against an American-style free-for-all in radio in which the goal was to attract the largest audiences and thereby secure the greatest advertising revenue. There was no paid advertising on the BBC; all the revenue came from a tax on receiving sets. Highbrow audiences, however, greatly enjoyed it. At a time when American, Australian and Canadian stations were drawing huge audiences cheering for their local teams with the broadcast of baseball, rugby and hockey, the BBC emphasized service for a national, rather than a regional audience. Boat races were well covered along with tennis and horse racing, but the BBC was reluctant to spend its severely limited air time on long football or cricket games, regardless of their popularity.The success of broadcasting provoked animosities between the BBC and well established media such as theatres, concert halls and the recording industry. By 1929, the BBC complained that the agents of many comedians refused to sign contracts for broadcasting, because they feared it harmed the artist "by making his material stale" and that it "reduces the value of the artist as a visible music-hall performer". On the other hand, the BBC was "keenly interested" in a cooperation with the recording companies who "in recent years ... have not been slow to make records of singers, orchestras, dance bands, etc. who have already proved their power to achieve popularity by wireless." Radio plays were so popular that the BBC had received 6,000 manuscripts by 1929, most of them written for stage and of little value for broadcasting: "Day in and day out, manuscripts come in, and nearly all go out again through the post, with a note saying 'We regret, etc.'" In the 1930s music broadcasts also enjoyed great popularity, for example the friendly and wide-ranging organ broadcasts at St George's Hall, Langham Place, by Reginald Foort, who held the official role of BBC Staff Theatre Organist from 1936 to 1938; Foort continued to work for the BBC as a freelance into the 1940s and enjoyed a nationwide following.Experimental television broadcasts were started in 1932, using an electromechanical 30-line system developed by John Logie Baird. Limited regular broadcasts using this system began in 1934, and an expanded service (now named the BBC Television Service) started from Alexandra Palace in 1936, alternating between an improved Baird mechanical 240 line system and the all electronic 405 line Marconi-EMI system. The superiority of the electronic system saw the mechanical system dropped early the following year.Television broadcasting was suspended from 1 September 1939 to 7 June 1946, during the Second World War, and it was left to BBC Radio broadcasters such as Reginald Foort to keep the nation's spirits up. The BBC moved much of its radio operations out of London, initially to Bristol, and then to Bedford. Concerts were broadcast from the Corn Exchange; the Trinity Chapel in St Paul's Church, Bedford was the studio for the daily service from 1941 to 1945 and, in the darkest days of the war in 1941, the Archbishops of Canterbury and York came to St Paul's to broadcast to the UK and all parts of the world on the National Day of Prayer.There was a widely reported urban myth that, upon resumption of the BBC television service after the war, announcer Leslie Mitchell started by saying, "As I was saying before we were so rudely interrupted ..." In fact, the first person to appear when transmission resumed was Jasmine Bligh and the words said were "Good afternoon, everybody. How are you? Do you remember me, Jasmine Bligh ... ?"The European Broadcasting Union was formed on 12 February 1950, in Torquay with the BBC among the 23 founding broadcasting organisations.Competition to the BBC was introduced in 1955, with the commercial and independently operated television network of ITV. However, the BBC monopoly on radio services would persist until 8 October 1973 when under the control of the newly renamed Independent Broadcasting Authority (IBA) the UK's first Independent local radio station, LBC came on-air in the London area. As a result of the Pilkington Committee report of 1962, in which the BBC was praised for the quality and range of its output, and ITV was very heavily criticised for not providing enough quality programming, the decision was taken to award the BBC a second television channel, BBC2, in 1964, renaming the existing service BBC1. BBC2 used the higher resolution 625 line standard which had been standardised across Europe. BBC2 was broadcast in colour from 1 July 1967, and was joined by BBC1 and ITV on 15 November 1969. The 405 line VHF transmissions of BBC1 (and ITV) were continued for compatibility with older television receivers until 1985.Starting in 1964, a series of pirate radio stations (starting with Radio Caroline) came on the air and forced the British government finally to regulate radio services to permit nationally based advertising-financed services. In response, the BBC reorganised and renamed their radio channels. On 30 September 1967, the Light Programme was split into Radio 1 offering continuous "Popular" music and Radio 2 more "Easy Listening". The "Third" programme became Radio 3 offering classical music and cultural programming. The Home Service became Radio 4 offering news, and non-musical content such as quiz shows, readings, dramas and plays. As well as the four national channels, a series of local BBC radio stations were established in 1967, including Radio London.In 1969, the BBC Enterprises department was formed to exploit BBC brands and programmes for commercial spin-off products. In 1979, it became a wholly owned limited company, BBC Enterprises Ltd.In 1974, the BBC's teletext service, Ceefax, was introduced, created initially to provide subtitling, but developed into a news and information service. In 1978, BBC staff went on strike just before the Christmas of that year, thus blocking out the transmission of both channels and amalgamating all four radio stations into one.Since the deregulation of the UK television and radio market in the 1980s, the BBC has faced increased competition from the commercial sector (and from the advertiser-funded public service broadcaster Channel 4), especially on satellite television, cable television, and digital television services.[citation needed]In the late 1980s, the BBC began a process of divestment by spinning off and selling parts of its organisation. In 1988, it sold off the Hulton Press Library, a photographic archive which had been acquired from the Picture Post magazine by the BBC in 1957. The archive was sold to Brian Deutsch and is now owned by Getty Images. During the 1990s, this process continued with the separation of certain operational arms of the corporation into autonomous but wholly owned subsidiaries of the BBC, with the aim of generating additional revenue for programme-making. BBC Enterprises was reorganised and relaunched in 1995, as BBC Worldwide Ltd. In 1998, BBC studios, outside broadcasts, post production, design, costumes and wigs were spun off into BBC Resources Ltd.The BBC Research Department has played a major part in the development of broadcasting and recording techniques. In the early days, it carried out essential research into acoustics and programme level and noise measurement.[citation needed] The BBC was also responsible for the development of the NICAM stereo standard.In recent decades, a number of additional channels and radio stations have been launched: Radio 5 was launched in 1990, as a sports and educational station, but was replaced in 1994, with Radio 5 Live, following the success of the Radio 4 service to cover the 1991 Gulf War. The new station would be a news and sport station. In 1997, BBC News 24, a rolling news channel, launched on digital television services and the following year, BBC Choice launched as the third general entertainment channel from the BBC. The BBC also purchased The Parliamentary Channel, which was renamed BBC Parliament. In 1999, BBC Knowledge launched as a multi media channel, with services available on the newly launched BBC Text digital teletext service, and on BBC Online. The channel had an educational aim, which was modified later on in its life to offer documentaries.In 2002, several television and radio channels were reorganised. BBC Knowledge was replaced by BBC Four and became the BBC's arts and documentaries channel. CBBC, which had been a programming strand as Children's BBC since 1985, was split into CBBC and CBeebies, for younger children, with both new services getting a digital channel: the CBBC Channel and CBeebies Channel. In addition to the television channels, new digital radio stations were created: 1Xtra, 6 Music and BBC7. BBC 1Xtra was a sister station to Radio 1 and specialised in modern black music, BBC 6 Music specialised in alternative music genres and BBC7 specialised in archive, speech and children's programming.The following few years resulted in repositioning of some of the channels to conform to a larger brand: in 2003, BBC Choice was replaced by BBC Three, with programming for younger generations and shocking real life documentaries, BBC News 24 became the BBC News Channel in 2008, and BBC Radio 7 became BBC Radio 4 Extra in 2011, with new programmes to supplement those broadcast on Radio 4. In 2008, another channel was launched, BBC Alba, a Scottish Gaelic service.During this decade, the corporation began to sell off a number of its operational divisions to private owners; BBC Broadcast was spun off as a separate company in 2002, and in 2005. it was sold off to Australian-based Macquarie Capital Alliance Group and Macquarie Bank Limited and rebranded Red Bee Media. The BBC's IT, telephony and broadcast technology were brought together as BBC Technology Ltd in 2001, and the division was later sold to the German engineering and electronics company Siemens IT Solutions and Services (SIS). SIS was subsequently acquired from Siemens by the French company Atos. Further divestments in this decade included BBC Books (sold to Random House in 2006); BBC Outside Broadcasts Ltd (sold in 2008. to Satellite Information Services); Costumes and Wigs (stock sold in 2008 to Angels The Costumiers); and BBC Magazines (sold to Immediate Media Company in 2011). After the sales of OBs and costumes, the remainder of BBC Resources was reorganised as BBC Studios and Post Production, which continues today as a wholly owned subsidiary of the BBC.The 2004 Hutton Inquiry and the subsequent Report raised questions about the BBC's journalistic standards and its impartiality. This led to resignations of senior management members at the time including the then Director General, Greg Dyke. In January 2007, the BBC released minutes of the board meeting which led to Greg Dyke's resignation.Unlike the other departments of the BBC, the BBC World Service was funded by the Foreign and Commonwealth Office. The Foreign and Commonwealth Office, more commonly known as the Foreign Office or the FCO, is the British government department responsible for promoting the interests of the United Kingdom abroad.In 2006, BBC HD launched as an experimental service, and became official in December 2007. The channel broadcast HD simulcasts of programmes on BBC One, BBC Two, BBC Three and BBC Four as well as repeats of some older programmes in HD. In 2010, an HD simulcast of BBC One launched: BBC One HD. The channel uses HD versions of BBC One's schedule and uses upscaled versions of programmes not currently produced in HD. The BBC HD channel closed in March 2013 and was replaced by BBC2 HD in the same month.On 18 October 2007, BBC Director General Mark Thompson announced a controversial plan to make major cuts and reduce the size of the BBC as an organisation. The plans included a reduction in posts of 2,500; including 1,800 redundancies, consolidating news operations, reducing programming output by 10% and selling off the flagship Television Centre building in London. These plans have been fiercely opposed by unions, who have threatened a series of strikes; however, the BBC have stated that the cuts are essential to move the organisation forward and concentrate on increasing the quality of programming.On 20 October 2010, the Chancellor of the Exchequer George Osborne announced that the television licence fee would be frozen at its current level until the end of the current charter in 2016. The same announcement revealed that the BBC would take on the full cost of running the BBC World Service and the BBC Monitoring service from the Foreign and Commonwealth Office, and partially finance the Welsh broadcaster S4C.Further cuts were announced on 6 October 2011, so the BBC could reach a total reduction in their budget of 20%, following the licence fee freeze in October 2010, which included cutting staff by 2,000 and sending a further 1,000 to the MediaCityUK development in Salford, with BBC Three moving online only in 2016, the sharing of more programmes between stations and channels, sharing of radio news bulletins, more repeats in schedules, including the whole of BBC Two daytime and for some original programming to be reduced. BBC HD was closed on 26 March 2013, and replaced with an HD simulcast of BBC Two; however, flagship programmes, other channels and full funding for CBBC and CBeebies would be retained. Numerous BBC facilities have been sold off, including New Broadcasting House on Oxford Road in Manchester. Many major departments have been relocated to Broadcasting House and MediaCityUK, particularly since the closure of BBC Television Centre in March 2013. The cuts inspired campaigns, petitions and protests such as SaveBBC3 and SaveOurBBC, which have built a following of hundreds of thousands of individuals concerned about the changes.The BBC is a statutory corporation, independent from direct government intervention, with its activities being overseen by the BBC Trust (formerly the Board of Governors). General management of the organisation is in the hands of a Director-General, appointed by the Trust, who is the BBC's Editor-in-Chief and chairs the Executive Board.The BBC operates under a Royal Charter. The current Charter came into effect on 1 January 2007 and runs until 31 December 2016. Each successive Royal Charter is reviewed before a new one is granted, i.e. every 10 years.The 2007 Charter specifies that the mission of the Corporation is to "inform, educate and entertain". It states that the Corporation exists to serve the public interest and to promote its public purposes: sustaining citizenship and civil society, promoting education and learning, stimulating creativity and cultural excellence, representing the UK, its nations, regions and communities, bringing the UK to the world and the world to the UK, helping to deliver to the public the benefit of emerging communications technologies and services, and taking a leading role in the switchover to digital television.The 2007 Charter made the largest change in the governance of the Corporation since its inception. It abolished the sometimes controversial governing body, the Board of Governors, replacing it with the sometimes controversial BBC Trust and a formalised Executive Board.Under the Royal Charter, the BBC must obtain a licence from the Home Secretary. This licence is accompanied by an agreement which sets the terms and conditions under which the BBC is allowed to broadcast. It was under this Licence and Agreement (and the Broadcasting Act 1981) that the Sinn F in broadcast ban from 1988 to 1994 was implemented.The BBC Trust was formed on 1 January 2007, replacing the Board of Governors as the governing body of the Corporation. The Trust sets the strategy for the corporation, assesses the performance of the BBC Executive Board in delivering the BBC's services, and appoints the Director-General.BBC Trustees are appointed by the British monarch on advice of government ministers. There are twelve trustees, led by Chairman Rona Fairhead who was appointed on 31 August 2014 and vice-chairman Sir Roger Carr. There are trustees for the four nations of the United Kingdom; England (Mark Florman), Scotland (Bill Matthews), Wales (Elan Closs Stephens) and Northern Ireland (Aideen McGinley). The remaining trustees are Sonita Alleyne, Richard Ayre, Mark Damazer, Nicholas Prettejohn, Suzanna Taverne and Lord Williams.The Executive Board meets once per month and is responsible for operational management and delivery of services within a framework set by the BBC Trust, and is headed by the Director-General, currently Tony Hall. The Executive Board consists of both Executive and Non-Executive directors, with non-executive directors being sourced from other companies and corporations and being appointed by the BBC Trust. The executive board is made up of the Director General as well as the head of each of the main BBC divisions. These at present are:The board shares some of its responsibilities to four sub-committees including: Audit, Fair Trading, Nominations and Remuneration.It is also supported by a number of management groups within the BBC, including the BBC Management Board, the Finance and Business committee, and boards at the Group level, such as Radio and Television. The boards of BBC Worldwide support and BBC Commercial Holdings along with the Executive Board on commercial matters.The management board is responsible for managing pan-BBC issues delegated to it from the executive board and ensures that the corporation meets its strategic objectives, the board meets three times per month. Current members include:The Corporation is headed by the Executive Board, which has overall control of the management and running of the BBC. Below this is the BBC Management board, which deals with inter departmental issues and any other tasks which the Executive board has delegated to it. Below the BBC Management board are the following six major divisions covering all the BBC's output:All aspects of the BBC fall into one or more of the above departments, with the following exceptions:The BBC has the second largest budget of any UK-based broadcaster with an operating expenditure of  4.722 billion in 2013/14 compared to  6.471 billion for British Sky Broadcasting in 2013/14 and  1.843 billion for ITV in the calendar year 2013.The principal means of funding the BBC is through the television licence, costing  145.50 per year per household since April 2010. Such a licence is required to legally receive broadcast television across the UK, the Channel Islands and the Isle of Man. No licence is required to own a television used for other means, or for sound only radio sets (though a separate licence for these was also required for non-TV households until 1971). The cost of a television licence is set by the government and enforced by the criminal law. A discount is available for households with only black-and-white television sets. A 50% discount is also offered to people who are registered blind or severely visually impaired, and the licence is completely free for any household containing anyone aged 75 or over. As a result of the UK Government's recent spending review, an agreement has been reached between the government and the corporation in which the current licence fee will remain frozen at the current level until the Royal Charter is renewed at the beginning of 2017.The revenue is collected privately[clarification needed] and is paid into the central government Consolidated Fund, a process defined in the Communications Act 2003. The BBC pursues its licence fee collection and enforcement under the trading name "TV Licensing". TV Licensing collection is currently carried out by Capita, an outside agency. Funds are then allocated by the Department of Culture, Media and Sport (DCMS) and the Treasury and approved by Parliament via legislation. Additional revenues are paid by the Department for Work and Pensions to compensate for subsidised licences for eligible over-75-year-olds.The licence fee is classified as a tax, and its evasion is a criminal offence. Since 1991, collection and enforcement of the licence fee has been the responsibility of the BBC in its role as TV Licensing Authority. Thus, the BBC is a major prosecuting authority in England and Wales and an investigating authority in the UK as a whole. The BBC carries out surveillance (mostly using subcontractors) on properties (under the auspices of the Regulation of Investigatory Powers Act 2000) and may conduct searches of a property using a search warrant. According to the BBC, "more than 204,000 people in the UK were caught watching TV without a licence during the first six months of 2012." Licence fee evasion makes up around one tenth of all cases prosecuted in magistrate courts.Income from commercial enterprises and from overseas sales of its catalogue of programmes has substantially increased over recent years, with BBC Worldwide contributing some  145 million to the BBC's core public service business.According to the BBC's 2013/14 Annual Report, its total income was  5 billion ( 5.066 billion), which can be broken down as follows:The licence fee has, however, attracted criticism. It has been argued that in an age of multi stream, multi-channel availability, an obligation to pay a licence fee is no longer appropriate. The BBC's use of private sector company Capita Group to send letters to premises not paying the licence fee has been criticised, especially as there have been cases where such letters have been sent to premises which are up to date with their payments, or do not require a TV licence.The BBC uses advertising campaigns to inform customers of the requirement to pay the licence fee. Past campaigns have been criticised by Conservative MP Boris Johnson and former MP Ann Widdecombe, for having a threatening nature and language used to scare evaders into paying. Audio clips and television broadcasts are used to inform listeners of the BBC's comprehensive database. There are a number of pressure groups campaigning on the issue of the licence fee.The majority of the BBC's commercial output comes from its commercial arm BBC Worldwide who sell programmes abroad and exploit key brands for merchandise. Of their 2012/13 sales, 27% were centred on the five key 'superbrands' of Doctor Who, Top Gear, Strictly Come Dancing (known as Dancing with the Stars internationally), the BBC's archive of natural history programming (collected under the umbrella of BBC Earth) and the, now sold, travel guide brand Lonely Planet.The following expenditure figures are from 2012/13 and show the expenditure of each service they are obliged to provide:A significantly large portion of the BBC's income is spent on the corporation's Television and Radio services with each service having a different budget based upon their content.Broadcasting House in Portland Place, London, is the official headquarters of the BBC. It is home to six of the ten BBC national radio networks, BBC Radio 1, BBC Radio 1xtra, BBC Asian Network, BBC Radio 3, BBC Radio 4, and BBC Radio 4 Extra. It is also the home of BBC News, which relocated to the building from BBC Television Centre in 2013. On the front of the building are statues of Prospero and Ariel, characters from William Shakespeare's play The Tempest, sculpted by Eric Gill. Renovation of Broadcasting House began in 2002, and was completed in 2013.Until it closed at the end of March 2013, BBC Television was based at BBC Television Centre, a purpose built television facility and the second built in the country located in White City, London. This facility has been host to a number of famous guests and programmes through the years, and its name and image is familiar with many British citizens. Nearby, the BBC White City complex contains numerous programme offices, housed in Centre House, the Media Centre and Broadcast Centre. It is in this area around Shepherd's Bush that the majority of BBC employees work.As part of a major reorganisation of BBC property, the entire BBC News operation relocated from the News Centre at BBC Television Centre to the refurbished Broadcasting House to create what is being described as "one of the world's largest live broadcast centres". The BBC News Channel and BBC World News relocated to the premises in early 2013. Broadcasting House is now also home to most of the BBC's national radio stations, and the BBC World Service. The major part of this plan involves the demolition of the two post-war extensions to the building and construction of an extension designed by Sir Richard MacCormac of MJP Architects. This move will concentrate the BBC's London operations, allowing them to sell Television Centre, which is expected to be completed by 2016.In addition to the scheme above, the BBC is in the process of making and producing more programmes outside London, involving production centres such as Belfast, Cardiff, Glasgow and, most notably, in Greater Manchester as part of the 'BBC North Project' scheme where several major departments, including BBC North West, BBC Manchester, BBC Sport, BBC Children's, CBeebies, Radio 5 Live, BBC Radio 5 Live Sports Extra, BBC Breakfast, BBC Learning and the BBC Philharmonic have all moved from their previous locations in either London or New Broadcasting House, Manchester to the new 200-acre (80ha) MediaCityUK production facilities in Salford, that form part of the large BBC North Group division and will therefore become the biggest staffing operation outside London.As well as the two main sites in London (Broadcasting House and White City), there are seven other important BBC production centres in the UK, mainly specialising in different productions. Broadcasting House Cardiff, has been home to BBC Cymru Wales, which specialises in drama production. Open since October 2011, and containing 7 new studios, Roath Lock is notable as the home of productions such as Doctor Who and Casualty. Broadcasting House Belfast, home to BBC Northern Ireland, specialises in original drama and comedy, and has taken part in many co-productions with independent companies and notably with RT  in the Republic of Ireland. BBC Scotland, based in Pacific Quay, Glasgow is a large producer of programmes for the network, including several quiz shows. In England, the larger regions also produce some programming.Previously, the largest 'hub' of BBC programming from the regions is BBC North West. At present they produce all Religious and Ethical programmes on the BBC, as well as other programmes such as A Question of Sport. However, this is to be merged and expanded under the BBC North project, which involved the region moving from New Broadcasting House, Manchester, to MediaCityUK. BBC Midlands, based at The Mailbox in Birmingham, also produces drama and contains the headquarters for the English regions and the BBC's daytime output. Other production centres include Broadcasting House Bristol, home of BBC West and famously the BBC Natural History Unit and to a lesser extent, Quarry Hill in Leeds, home of BBC Yorkshire. There are also many smaller local and regional studios throughout the UK, operating the BBC regional television services and the BBC Local Radio stations.The BBC also operates several news gathering centres in various locations around the world, which provide news coverage of that region to the national and international news operations.In 2004, the BBC contracted out its former BBC Technology division to the German engineering and electronics company Siemens IT Solutions and Services (SIS), outsourcing its IT, telephony and broadcast technology systems. When Atos Origin acquired the SIS division from Siemens in December 2010 for  850 million ( 720m), the BBC support contract also passed to Atos, and in July 2011, the BBC announced to staff that its technology support would become an Atos service. Siemens staff working on the BBC contract were transferred to Atos and BBC technology systems (including the BBC website) are now managed by Atos. In 2011, the BBC's Chief Financial Officer Zarin Patel stated to the House of Commons Public Accounts Committee that, following criticism of the BBC's management of major IT projects with Siemens (such as the Digital Media Initiative), the BBC partnership with Atos would be instrumental in achieving cost savings of around  64 million as part of the BBC's "Delivering Quality First" programme. In 2012, the BBC's Chief Technology Officer, John Linwood, expressed confidence in service improvements to the BBC's technology provision brought about by Atos. He also stated that supplier accountability had been strengthened following some high-profile technology failures which had taken place during the partnership with Siemens.The BBC operates several television channels in the UK of which BBC One and BBC Two are the flagship television channels. In addition to these two flagship channels, the BBC operates several digital only stations: BBC Four, BBC News, BBC Parliament, and two children's channels, CBBC and CBeebies. Digital television is now in widespread use in the UK, with analogue transmission completely phased out by December 2012. It also operates the internet television service BBC Three, which ceased broadcasting as a linear television channel in February 2016.BBC One is a regionalised TV service which provides opt-outs throughout the day for local news and other local programming. These variations are more pronounced in the BBC 'Nations', i.e. Northern Ireland, Scotland and Wales, where the presentation is mostly carried out locally on BBC One and Two, and where programme schedules can vary largely from that of the network. BBC Two variations exist in the Nations; however, English regions today rarely have the option to 'opt out' as regional programming now only exists on BBC One, and regional opt outs are not possible in the regions that have already undertaken the switch to digital television. BBC Two was also the first channel to be transmitted on 625 lines in 1964, then carry a small-scale regular colour service from 1967. BBC One would follow in November 1969.A new Scottish Gaelic television channel, BBC Alba, was launched in September 2008. It is also the first multi-genre channel to come entirely from Scotland with almost all of its programmes made in Scotland. The service was initially only available via satellite but since June 2011 has been available to viewers in Scotland on Freeview and cable television.The BBC currently operates HD simulcasts of all its nationwide channels with the exception of BBC Parliament. Until 26 March 2013, a separate channel called BBC HD was available, in place of BBC Two HD. It launched on 9 June 2006, following a 12-month trial of the broadcasts. It became a proper channel in 2007, and screened HD programmes as simulcasts of the main network, or as repeats. The corporation has been producing programmes in the format for many years, and stated that it hoped to produce 100% of new programmes in HDTV by 2010. On 3 November 2010, a high-definition simulcast of BBC One was launched, entitled BBC One HD, and BBC Two HD launched on 26 March 2013, replacing BBC HD.In the Republic of Ireland, Belgium, the Netherlands and Switzerland, the BBC channels are available in a number of ways. In these countries digital and cable operators carry a range of BBC channels. These include BBC One, BBC Two and BBC World News, although viewers in the Republic of Ireland may receive BBC services via 'overspill' from transmitters in Northern Ireland or Wales, or via 'deflectors' - transmitters in the Republic which rebroadcast broadcasts from the UK, received off-air, or from digital satellite.Since 1975, the BBC has also provided its TV programmes to the British Forces Broadcasting Service (BFBS), allowing members of UK military serving abroad to watch them on four dedicated TV channels. From 27 March 2013, BFBS will carry versions of BBC One and BBC Two, which will include children's programming from CBBC, as well as carrying programming from BBC Three on a new channel called BFBS Extra.Since 2008, all the BBC channels are available to watch online through the BBC iPlayer service. This online streaming ability came about following experiments with live streaming, involving streaming certain channels in the UK.In February 2014, Director-General Tony Hall announced that the corporation needed to save  100 million. In March 2014, the BBC confirmed plans for BBC Three to become an internet-only channel.In December 2012, the BBC completed a digitisation exercise, scanning the listings of all BBC programmes from an entire run of about 4,500 copies of the Radio Times magazine from the first, 1923, issue to 2009 (later listings already being held electronically), the 'BBC Genome project', with a view to creating an online database of its programme output. An earlier ten months of listings are to be obtained from other sources. They identified around five million programmes, involving 8.5 million actors, presenters, writers and technical staff. The Genome project was opened to public access on 15 October 2014, with corrections to OCR errors and changes to advertised schedules being crowdsourced.The BBC has ten radio stations serving the whole of the UK, a further six stations in the "national regions" (Wales, Scotland, and Northern Ireland), and 40 other local stations serving defined areas of England. Of the ten national stations, five are major stations and are available on FM and/or AM as well as on DAB and online. These are BBC Radio 1, offering new music and popular styles and being notable for its chart show; BBC Radio 2, playing Adult contemporary, country and soul music amongst many other genres; BBC Radio 3, presenting classical and jazz music together with some spoken-word programming of a cultural nature in the evenings; BBC Radio 4, focusing on current affairs, factual and other speech-based programming, including drama and comedy; and BBC Radio 5 Live, broadcasting 24-hour news, sport and talk programmes.In addition to these five stations, the BBC also runs a further five stations that broadcast on DAB and online only. These stations supplement and expand on the big five stations, and were launched in 2002. BBC Radio 1Xtra sisters Radio 1, and broadcasts new black music and urban tracks. BBC Radio 5 Live Sports Extra sisters 5 Live and offers extra sport analysis, including broadcasting sports that previously were not covered. BBC Radio 6 Music offers alternative music genres and is notable as a platform for new artists.BBC Radio 7, later renamed BBC Radio 4 Extra, provided archive drama, comedy and children's programming. Following the change to Radio 4 Extra, the service has dropped a defined children's strand in favour of family-friendly drama and comedy. In addition, new programmes to complement Radio 4 programmes were introduced such as Ambridge Extra, and Desert Island Discs revisited. The final station is the BBC Asian Network, providing music, talk and news to this section of the community. This station evolved out of Local radio stations serving certain areas, and as such this station is available on Medium Wave frequency in some areas of the Midlands.As well as the national stations, the BBC also provides 40 BBC Local Radio stations in England and the Channel Islands, each named for and covering a particular city and its surrounding area (e.g. BBC Radio Bristol), county or region (e.g. BBC Three Counties Radio), or geographical area (e.g. BBC Radio Solent covering the central south coast). A further six stations broadcast in what the BBC terms "the national regions": Wales, Scotland, and Northern Ireland. These are BBC Radio Wales (in English), BBC Radio Cymru (in Welsh), BBC Radio Scotland (in English), BBC Radio nan Gaidheal (in Scottish Gaelic), BBC Radio Ulster, and BBC Radio Foyle, the latter being an opt-out station from Radio Ulster for the north-west of Northern Ireland.The BBC's UK national channels are also broadcast in the Channel Islands and the Isle of Man (although these Crown dependencies are outside the UK), and in the former there are two local stations - BBC Guernsey and BBC Radio Jersey. There is no BBC local radio station, however, in the Isle of Man, partly because the island has long been served by the popular independent commercial station, Manx Radio, which predates the existence of BBC Local Radio. BBC services in the dependencies are financed from television licence fees which are set at the same level as those payable in the UK, although collected locally. This is the subject of some controversy in the Isle of Man since, as well as having no BBC Local Radio service, the island also lacks a local television news service analogous to that provided by BBC Channel Islands.For a worldwide audience, the BBC World Service provides news, current affairs and information in 28 languages, including English, around the world and is available in over 150 capital cities. It is broadcast worldwide on shortwave radio, DAB and online and has an estimated weekly audience of 192 million, and its websites have an audience of 38 million people per week. Since 2005, it is also available on DAB in the UK, a step not taken before, due to the way it is funded. The service is funded by a Parliamentary Grant-in-Aid, administered by the Foreign Office; however, following the Government's spending review in 2011, this funding will cease, and it will be funded for the first time through the Licence fee. In recent years, some services of the World Service have been reduced; the Thai service ended in 2006, as did the Eastern European languages, with resources diverted instead into the new BBC Arabic  the BBC was the only legal radio broadcaster based in the UK mainland until 1967, when University Radio York (URY), then under the name Radio York, was launched as the first, and now oldest, legal independent radio station in the country. However, the BBC did not enjoy a complete monopoly before this as several Continental stations, such as Radio Luxembourg, had broadcast programmes in English to Britain since the 1930s and the Isle of Man-based Manx Radio began in 1964. Today, despite the advent of commercial radio, BBC radio stations remain among the most listened to in the country, with Radio 2 having the largest audience share (up to 16.8% in 2011-12) and Radios 1 and 4 ranked second and third in terms of weekly reach.BBC programming is also available to other services and in other countries. Since 1943, the BBC has provided radio programming to the British Forces Broadcasting Service, which broadcasts in countries where British troops are stationed. BBC Radio 1 is also carried in the United States and Canada on Sirius XM Radio (online streaming only).The BBC is a patron of The Radio Academy.BBC News is the largest broadcast news gathering operation in the world, providing services to BBC domestic radio as well as television networks such as the BBC News, BBC Parliament and BBC World News. In addition to this, news stories are available on the BBC Red Button service and BBC News Online. In addition to this, the BBC has been developing new ways to access BBC News, as a result has launched the service on BBC Mobile, making it accessible to mobile phones and PDAs, as well as developing alerts by e-mail, digital television, and on computers through a desktop alert.Ratings figures suggest that during major incidents such as the 7 July 2005 London bombings or royal events, the UK audience overwhelmingly turns to the BBC's coverage as opposed to its commercial rivals. On 7 July 2005, the day that there were a series of coordinated bomb blasts on London's public transport system, the BBC Online website recorded an all time bandwidth peak of 11 Gb/s at 12.00 on 7 July. BBC News received some 1 billion total hits on the day of the event (including all images, text and HTML), serving some 5.5 terabytes of data. At peak times during the day there were 40,000 page requests per second for the BBC News website. The previous day's announcement of the 2012 Olympics being awarded to London caused a peak of around 5 Gbit/s. The previous all-time high at BBC Online was caused by the announcement of the Michael Jackson verdict, which used 7.2 Gbit/s.The BBC's online presence includes a comprehensive news website and archive. It was launched as BBC Online, before being renamed BBCi, then bbc.co.uk, before it was rebranded back as BBC Online. The website is funded by the Licence fee, but uses GeoIP technology, allowing advertisements to be carried on the site when viewed outside of the UK. The BBC claims the site to be "Europe's most popular content-based site" and states that 13.2 million people in the UK visit the site's more than two million pages each day. According to Alexa's TrafficRank system, in July 2008 BBC Online was the 27th most popular English Language website in the world, and the 46th most popular overall.The centre of the website is the Homepage, which features a modular layout. Users can choose which modules, and which information, is displayed on their homepage, allowing the user to customise it. This system was first launched in December 2007, becoming permanent in February 2008, and has undergone a few aesthetical changes since then. The Homepage then has links to other micro-sites, such as BBC News Online, Sport, Weather, TV and Radio. As part of the site, every programme on BBC Television or Radio is given its own page, with bigger programmes getting their own micro-site, and as a result it is often common for viewers and listeners to be told website addresses (URLs) for the programme website.Another large part of the site also allows users to watch and listen to most Television and Radio output live and for seven days after broadcast using the BBC iPlayer platform, which launched on 27 July 2007, and initially used peer-to-peer and DRM technology to deliver both radio and TV content of the last seven days for offline use for up to 30 days, since then video is now streamed directly. Also, through participation in the Creative Archive Licence group, bbc.co.uk allowed legal downloads of selected archive material via the internet.The BBC has often included learning as part of its online service, running services such as BBC Jam, Learning Zone Class Clips and also runs services such as BBC WebWise and First Click which are designed to teach people how to use the internet. BBC Jam was a free online service, delivered through broadband and narrowband connections, providing high-quality interactive resources designed to stimulate learning at home and at school. Initial content was made available in January 2006; however, BBC Jam was suspended on 20 March 2007 due to allegations made to the European Commission that it was damaging the interests of the commercial sector of the industry.In recent years, some major on-line companies and politicians have complained that BBC Online receives too much funding from the television licence, meaning that other websites are unable to compete with the vast amount of advertising-free on-line content available on BBC Online. Some have proposed that the amount of licence fee money spent on BBC Online should be reduced-either being replaced with funding from advertisements or subscriptions, or a reduction in the amount of content available on the site. In response to this the BBC carried out an investigation, and has now set in motion a plan to change the way it provides its online services. BBC Online will now attempt to fill in gaps in the market, and will guide users to other websites for currently existing market provision. (For example, instead of providing local events information and timetables, users will be guided to outside websites already providing that information.) Part of this plan included the BBC closing some of its websites, and rediverting money to redevelop other parts.On 26 February 2010, The Times claimed that Mark Thompson, Director General of the BBC, proposed that the BBC's web output should be cut by 50%, with online staff numbers and budgets reduced by 25% in a bid to scale back BBC operations and allow commercial rivals more room. On 2 March 2010, the BBC reported that it will cut its website spending by 25% and close BBC 6 Music and Asian Network, as part of Mark Thompson's plans to make "a smaller, fitter BBC for the digital age".BBC Red Button is the brand name for the BBC's interactive digital television services, which are available through Freeview (digital terrestrial), as well as Freesat, Sky (satellite), and Virgin Media (cable). Unlike Ceefax, the service's analogue counterpart, BBC Red Button is able to display full-colour graphics, photographs, and video, as well as programmes and can be accessed from any BBC channel. The service carries News, Weather and Sport 24 hours a day, but also provides extra features related to programmes specific at that time. Examples include viewers to play along at home to gameshows, to give, voice and vote on opinions to issues, as used alongside programmes such as Question Time. At some points in the year, when multiple sporting events occur, some coverage of less mainstream sports or games are frequently placed on the Red Button for viewers to watch. Frequently, other features are added unrelated to programmes being broadcast at that time, such as the broadcast of the Doctor Who animated episode Dreamland in November 2009.The BBC employs staff orchestras, a choir, and supports two amateur choruses, based in BBC venues across the UK; the BBC Symphony Orchestra, the BBC Singers, BBC Symphony Chorus and BBC Big Band based in London, the BBC Scottish Symphony Orchestra in Glasgow, the BBC Philharmonic in Manchester, the BBC Concert Orchestra based in Watford and the BBC National Orchestra of Wales in Cardiff. It also buys a selected number of broadcasts from the Ulster Orchestra in Belfast. Many famous musicians of every genre have played at the BBC, such as The Beatles (The Beatles Live at the BBC is one of their many albums). The BBC is also responsible for the United Kingdom coverage of the Eurovision Song Contest, a show with which the broadcaster has been associated for over 50 years. The BBC also operates the division of BBC Audiobooks sometimes found in association with Chivers Audiobooks.The BBC operates other ventures in addition to their broadcasting arm. In addition to broadcasting output on television and radio, some programmes are also displayed on the BBC Big Screens located in several central-city locations. The BBC and the Foreign and Commonwealth Office also jointly run BBC Monitoring, which monitors radio, television, the press and the internet worldwide. The BBC also developed several computers throughout the 1980s, most notably the BBC Micro, which ran alongside the corporation's educational aims and programming.In 1951, in conjunction with Oxford University Press the BBC published The BBC Hymn Book which was intended to be used by radio listeners to follow hymns being broadcast. The book was published both with and without music, the music edition being entitled The BBC Hymn Book with Music. The book contained 542 popular hymns.The BBC provided the world's first teletext service called Ceefax (near-homonymous with "See Facts") on 23 September 1974 until 23 October 2012 on the BBC 1 analogue channel then later on BBC 2. It showed informational pages such as News, Sport and the Weather. on New Year's Eve in 1974, competition from ITV's Oracle tried to compete with Ceefax. Oracle closed on New Year's Eve, 1992. During its lifetime it attracted millions of viewers, right up to 2012, prior to the digital switchover in the United Kingdom. It ceased transmission at 23:32:19 BST on 23 October 2012 after 38 years. Since then, the BBC's Red Button Service has provided a digital-like information system that replaced Ceefax.Britflix is an upcoming online video streaming service by the BBC.BBC Worldwide Limited is the wholly owned commercial subsidiary of the BBC, responsible for the commercial exploitation of BBC programmes and other properties, including a number of television stations throughout the world. It was formed following the restructuring of its predecessor, BBC Enterprises, in 1995.The company owns and administers a number of commercial stations around the world operating in a number of territories and on a number of different platforms. The channel BBC Entertainment shows current and archive entertainment programming to viewers in Europe, Africa, Asia and the Middle East, with the BBC Worldwide channels BBC America and BBC Canada (Joint venture with Corus Entertainment) showing similar programming in the North America region and BBC UKTV in the Australasia region. The company also airs two channels aimed at children, an international CBeebies channel and BBC Kids, a joint venture with Knowledge Network Corporation, which airs programmes under the CBeebies and BBC K brands. The company also runs the channels BBC Knowledge, broadcasting factual and learning programmes, and BBC Lifestyle, broadcasting programmes based on themes of Food, Style and Wellbeing. In addition to this, BBC Worldwide runs an international version of the channel BBC HD, and provides HD simulcasts of the channels BBC Knowledge and BBC America.BBC Worldwide also distributes the 24-hour international news channel BBC World News. The station is separate from BBC Worldwide to maintain the station's neutral point of view, but is distributed by BBC Worldwide. The channel itself is the oldest surviving entity of its kind, and has 50 foreign news bureaus and correspondents in nearly all countries in the world. As officially surveyed it is available to more than 294 million households, significantly more than CNN's estimated 200 million.  In addition to these international channels, BBC Worldwide also owns, together with Scripps Networks Interactive, the UKTV network of ten channels. These channels contain BBC archive programming to be rebroadcast on their respective channels: Alibi, crime dramas; Drama, drama, launched in 2013; Dave (slogan: "The Home of Witty Banter"); Eden, nature; Gold, comedy; Good Food, cookery; Home, home and garden; Really, female programming; Watch, entertainment; and Yesterday, history programming.In addition to these channels, many BBC programmes are sold via BBC Worldwide to foreign television stations with comedy, documentaries and historical drama productions being the most popular. In addition, BBC television news appears nightly on many Public Broadcasting Service stations in the United States, as do reruns of BBC programmes such as EastEnders, and in New Zealand on TVNZ 1.In addition to programming, BBC Worldwide produces material to accompany programmes. The company maintained the publishing arm of the BBC, BBC Magazines, which published the Radio Times as well as a number of magazines that support BBC programming such as BBC Top Gear, BBC Good Food, BBC Sky at Night, BBC History, BBC Wildlife and BBC Music. BBC Magazines was sold to Exponent Private Equity in 2011, which merged it with Origin Publishing (previously owned by BBC Worldwide between 2004 and 2006) to form Immediate Media Company.BBC Worldwide also publishes books, to accompany programmes such as Doctor Who under the BBC Books brand, a publishing imprint majority owned by Random House. Soundtrack albums, talking books and sections of radio broadcasts are also sold under the brand BBC Records, with DVDs also being sold and licensed in large quantities to consumers both in the UK and abroad under the 2 Entertain brand. Archive programming and classical music recordings are sold under the brand BBC Legends.Until the development, popularisation, and domination of television, radio was the broadcast medium upon which people in the United Kingdom relied. It "reached into every home in the land, and simultaneously united the nation, an important factor during the Second World War". The BBC introduced the world's first "high-definition" 405-line television service in 1936. It suspended its television service during the Second World War and until 1946, but remained the only television broadcaster in the UK until 1955. "The BBC's monopoly was broken in 1955, with the introduction of Independent Television (ITV)". This heralded the transformation of television into a popular and dominant medium. Nevertheless, "throughout the 1950s radio still remained the dominant source of broadcast comedy". Further, the BBC was the only legal radio broadcaster until 1968 (when URY obtained their first licence).Despite the advent of commercial television and radio, the BBC has remained one of the main elements in British popular culture through its obligation to produce TV and radio programmes for mass audiences. However, the arrival of BBC2 allowed the BBC also to make programmes for minority interests in drama, documentaries, current affairs, entertainment, and sport. Examples cited include the television series Civilisation, Doctor Who, I, Claudius, Monty Python's Flying Circus, Pot Black, and Tonight, but other examples can be given in each of these fields as shown by the BBC's entries in the British Film Institute's 2000 list of the 100 Greatest British Television Programmes. The export of BBC programmes both through services like the BBC World Service and BBC World News, as well as through the channels operated by BBC Worldwide, means that audiences can consume BBC productions worldwide.The term "BBC English" was used as an alternative name for Received Pronunciation, and the English Pronouncing Dictionary uses the term "BBC Pronunciation" to label its recommendations. However, the BBC itself now makes more use of regional accents in order to reflect the diversity of the UK, while continuing to expect clarity and fluency of its presenters. From its "starchy" beginnings, the BBC has also become more inclusive, and now attempts to accommodate the interests of all strata of society and all minorities, because they all pay the licence fee.Competition from Independent Television, Channel 4, Sky, and other broadcast-television stations has lessened the BBC's influence, but its public broadcasting remains a major influence on British popular culture.Older domestic UK audiences often refer to the BBC as "the Beeb", a nickname originally coined by Peter Sellers on The Goon Show in the 1950s, when he referred to the "Beeb Beeb Ceeb". It was then borrowed, shortened and popularised by Kenny Everett. Another nickname, now less commonly used, is "Auntie", said to originate from the old-fashioned "Auntie knows best" attitude, or the idea of aunties and uncles who are present in the background of one's life (but possibly a reference to the "aunties" and "uncles" who presented children's programmes in the early days) in the days when John Reith, the BBC's first director general, was in charge. The two nicknames have also been used together as "Auntie Beeb".The BBC has faced various accusations regarding many topics: the Iraq war, politics, ethics and religion, as well as funding and staffing. It also has been involved in numerous controversies because of its different, sometimes very controversial coverage of specific news stories and programming. In October 2014, the BBC Trust issued the "BBC complaints framework", outlining complaints and appeals procedures. However, the regulatory oversight of the BBC may be transferred to OFCOM. The British "House of Commons Select Committee on Culture Media and Sport" recommended in its report "The Future of the BBC", that OFCOM should become the final arbiter of complaints made about the BBC.Accusations of a bias against the government and the Conservative Party were often made against the Corporation by members of Margaret Thatcher's 1980s Conservative government. BBC presenter Andrew Marr has said that "The BBC is not impartial or neutral. It has a liberal bias, not so much a party-political bias. It is better expressed as a cultural liberal bias." Conversely, the BBC has been criticised by The Guardian columnist, Owen Jones, who has said that "the truth is the BBC is stacked full of rightwingers." Paul Mason, the former Economics Editor of the BBC's Newsnight programme, has also criticised the BBC as "unionist" in relation to the BBC's coverage of the 2014 Scottish referendum campaign and "neo-liberal". However, Peter Sissons, a main news presenter at the BBC from 1989-2009, who from 1964-1989 worked as a journalist and then senior presenter at ITN, latterly at Channel 4 News, says "At the core of the BBC, in its very DNA, is a way of thinking that is firmly of the Left". The BBC has also been characterised as a pro-monarchist institution. The BBC was also accused of propaganda by journalist and author Toby Young, due to what he believed to be an anti-Brexit approach including a whole day of live programming on migration.The BBC World Service was involved in the Kyrgyz revolution in April 2010. One of the news presenters and a producer of the BBC World Service language, was revealed to have participated in the opposition movement at the time, with the goal to overthrow the Kyrgyzstan government led by president Kurmanbek Bakiyev using BBC resources. The BBC producer resigned from his post in 2010 once the news of his participation in the revolution became public. The BBC World Service neither confirmed nor denied this story, nor did the service issue a statement about this story. BBC documentary made by Justin Rowlatt, 'One World: Killing for Conservation' questions India s aggressive protection methods at Kaziranga National park, Assam. The documentary claimed that forest guards in this national park had been given authority to shoot and kill anyone, who would prove to be a threat to rhinos. The documentary was criticized by the Union environment for being "grossly erroneous". Following this, the National Conservation Authority (NTCA) in India imposed a ban on BBC and its journalist Justin Rowlatt for five years."""

###### MULTITHREADING EXPERIMENTS STUFF

manager = Manager()
# If there are fewer than four cores available for other things then 
# scrapy runspiders gets locked up
# We need one core for managing things, one core for running scrapy, and...
# maybe one core for scheduling scrapy jobs? And then I really have no idea what
# the fourth core is needed for.
pool = Pool(2)

parse_wiktionary_lock = manager.Lock()
shared_sentence_graph_count = manager.Value('L', 0)
shared_sentence_graphs_list = manager.list()

################################################################################
###########################-----Global Variables-----###########################
################################################################################

WIKIPEDIA_ARTICLE_LIST_FILE_PATH = "data/enwiki-latest-all-titles-in-ns0"
WIKIPEDIA_WEB_ROOT_URL = "https://en.wikipedia.org/wiki"
WIKIPEDIA_LOCAL_ROOT_URL = ""

WIKTIONARY_WEB_ROOT_URL = "https://en.wiktionary.org/wiki"
WIKTIONARY_LOCAL_ROOT_URL = ""
# The part of speech is the only string argument to this query
WIKTIONARY_XPATH_QUERY_H3 =\
"""//span[@class="mw-headline"][@id="English"]/../following-sibling::h3/span[@class="mw-headline"][@id="%s"]/../following-sibling::ol[1]/li[1]/node()[not(self::ul)][not(self::dl)]//self::text()[normalize-space()]"""
WIKTIONARY_XPATH_QUERY_H4 =\
"""//span[@class="mw-headline"][@id="English"]/../following-sibling::h4/span[@class="mw-headline"][@id="%s"]/../following-sibling::ol[1]/li[1]/node()[not(self::ul)][not(self::dl)]//self::text()[normalize-space()]"""
SHORT_WIKTIONARY_XPATH_QUERY_H3 =\
"""//span[@class="mw-headline"][@id="English"]/../following-sibling::h3/span[@class="mw-headline"][@id="%s"]"""
SHORT_WIKTIONARY_XPATH_QUERY_H4 =\
"""//span[@class="mw-headline"][@id="English"]/../following-sibling::h4/span[@class="mw-headline"][@id="%s"]"""

AYLIEN_APP_ID = "7fe8de1d"
AYLIEN_APP_KEY = "ef49f063d5cb17a97f158e43de5f7747"

PARSEY_PART_OF_SPEECH_TO_WIKTIONARY_MAP = {
    'CC': 'Conjunction',
    'CD': 'Cardinal number',
    'DT': 'Determiner',
    'EX': 'Existential there',
    'IN': 'Preposition',
    'JJ': 'Adjective',
    'JJR': 'Adjective',
    'JJS': 'Adjective',
    'LS': 'List item marker',
    'MD': 'Modal',
    'NN': 'Noun',
    'NNS': 'Noun',
    'NNP': 'Proper noun',
    'NNPS': 'Proper noun',
    'PDT': 'Predeterminer',
    'POS': 'Possessive ending',
    'PRP': 'Pronoun',
    'PRP$': 'Pronoun',
    'RB': 'Adverb',
    'RBR': 'Adverb',
    'RBS': 'Adverb',
    'RP': 'Particle',
    'SYM': 'Symbol',
    'TO': 'To',
    'UH': 'Interjection',
    'VB': 'Verb',
    'VBD': 'Verb',
    'VBG': 'Verb',
    'VBN': 'Verb',
    'VBP': 'Verb',
    'VBZ': 'Verb',
    'WDT': 'Determiner',
    'WP': 'Pronoun',
    'WP$': 'Pronoun',
    'WRB': 'Adverb',
}

################################################################################
###########################-----Scrapy Spider(s)-----###########################
################################################################################

# A scrapy spider for scraping a definition of a word from Wiktionary
# The definition is specified by the word and the part of speech, for now the
# language is assumed to be English.
# The definition is returned as a dict to go through scrapy's usual processing
# pipeline.
# To write the definition to file as JSON, set the following project settings 
# before initiating a crawl
# 
# settings = {
#        'FEED_FORMAT': 'json',
#        'FEED_URI': output_file_path,
#        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
# }
#
# NOTE: USER_AGENT is obviously unrelated to scrapy output, but it's included to
#       have all default settings in one place.
class WiktionarySpider(scrapy.Spider):
    name = "wiktionary-web"

    def __init__(self, *args, **kwargs):
        super(WiktionarySpider, self).__init__(*args, **kwargs)
        self.urls = kwargs.get('urls')
        self.word = kwargs.get('word')
        self.part_of_speech = kwargs.get('part_of_speech')
        self.output_file_path = kwargs.get('output_file_path')
        if not isinstance(self.urls, types.ListType):
            self.urls = [self.urls]
        
        # We don't want any strange characters like quotes
        self.word = filter(self._character_filter, self.word.lower())

        # Wiktionary has all part of speech headings with the first letter 
        # captialized and the other letters lowercase
        self.part_of_speech =\
            self.part_of_speech[:1].upper() + self.part_of_speech[1:].lower()

        self.log("\n\n")
        self.log("urls: %s" % self.urls)
        self.log("word: %s" % self.word)
        self.log("part_of_speech: %s" % self.part_of_speech)
        self.log("\n\n")

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(
                url=url, 
                callback=self.wiktionary_parse,
                errback=self.error_callback)

    def error_callback(self):
        self.log("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$Error callback reached")
        return None

    def wiktionary_parse(self, response):
        self.log("\n\n")
        self.log("Word: %s" % self.word)
        self.log("Part of Speech: %s\n" % self.part_of_speech)

        self.log("short wiktionary xpath result (h3): %s" %
            response
                .xpath(SHORT_WIKTIONARY_XPATH_QUERY_H3 % self.part_of_speech)
                .extract())

        xpath_parse = response\
            .xpath(WIKTIONARY_XPATH_QUERY_H3 % self.part_of_speech)\
            .extract()
        if len(xpath_parse) == 0:
            self.log("short wiktionary xpath result (h4): %s" %
                response
                    .xpath(SHORT_WIKTIONARY_XPATH_QUERY_H4 
                        % self.part_of_speech)
                    .extract())
            xpath_parse = response\
            .xpath(WIKTIONARY_XPATH_QUERY_H4 % self.part_of_speech)\
            .extract()
        definition = ' '\
            .join([x.strip() for x in xpath_parse])\
            .replace('.', '')\
            .strip()

        definition = filter(self._character_filter, definition.lower())

        self.log("Fully Parsed Definition: %s\n\n\n" % definition)

        output_dict = {
            'word': self.word,
            'part_of_speech': self.part_of_speech,
            'definition': definition,
        }

        #self._write_definition_json_to_file(output_dict, self.output_file_path)

        return output_dict

    def _write_definition_json_to_file(self, output_dict, output_file_path):
        print("Writing: %s to file" % output_dict)
        lock_pass = str(uuid.uuid1())
        file_lock = Locker(
            filePath=output_file_path, lockPass=lock_pass, mode='w')

        written = False
        while not written:
            with file_lock as lock:
                was_acquired, code, fd = lock
                # If lock was acquired
                if fd is not None:
                    fd.write(json.dumps([output_dict]))
                    written = True
                else:
                    time.sleep(1)

    def _character_filter(self, x):
        return ord('a') <= ord(x) <= ord('z')\
            or ord(x) == ord(' ')\
            or ord(x) == ord('<')\
            or ord(x) == ord('=')\
            or ord(x) == ord('>')\
            or ord(x) == ord('.')\
            or ord(x) == ord(',')

################################################################################
###########################-----Wikpedia Functions-----#########################
################################################################################

# Scrape all of wikipedia starting at a random page and going up to page_limit
# pages before stopping. If page_limit==0 then all of wikipedia will be scraped.
def scrape_wikipedia(
        wikipedia_root_url=WIKIPEDIA_WEB_ROOT_URL, 
        article_titles_file=WIKIPEDIA_ARTICLE_LIST_FILE_PATH, 
        page_limit=5):
    wikipedia_urls_generator = get_all_wikipedia_urls(\
        wikipedia_root_url,
        article_titles_file)

    wikipedia_articles = []
    url_count = 0
    for url in wikipedia_urls_generator:
        wikipedia_article_body = _strip_wikipedia_citations(\
            get_article_text(url))
        wikipedia_article_dict = {
            'url': url, 
            'body': wikipedia_article_body, 
            'sentence_graphs': list(),
        }
        wikipedia_articles.append(wikipedia_article_dict)

        url_count += 1
        if page_limit > 0 and url_count > page_limit:
            break

    return wikipedia_articles

# Return a generator that generates all wikipedia article URLs starting from the
# passed URL (for handling local copies of wikipedia or other mirrors) drawing 
# from the passed in article_titles_file to obtain a listing of page titles.
def get_all_wikipedia_urls(wikipedia_root_url, article_titles_file):
    with open(article_titles_file, 'r') as titles_file:
        for line in titles_file:
            yield "%s/%s" % (wikipedia_root_url, line)

# Use Aylien API to get text from URL or full text
#
# Return string with article text
def get_article_text(url):
    client = _get_aylien_client()
    return client.Extract(url)["article"]

def _get_aylien_client(
        aylien_app_id=AYLIEN_APP_ID, aylien_app_key=AYLIEN_APP_KEY):
    return textapi.Client(aylien_app_id, aylien_app_key)

# Strip Wikipedia citations from the passed in text
# e.g. [27], [309]
def _strip_wikipedia_citations(text):
    return re.sub("\[[0-9]*\]", "", text)

################################################################################
##########################-----Wiktionary Functions-----########################
################################################################################

# Hit wiktionary, scrape definition using word and POS
#
# Return a sentence graph of the definition
def lookup_definition_on_wiktionary(
        word, 
        part_of_speech, 
        wiktionary_root_url=WIKTIONARY_WEB_ROOT_URL,
        use_cache=True):
    print("Looking up %s %s on wiktionary......" % (word, part_of_speech))
    definition_text = _parse_wiktionary(
        "%s/%s" % (wiktionary_root_url, word), 
        word, 
        part_of_speech, 
        use_cache=use_cache)
    return definition_text

def _try_acquire_file_lock(folder_name, file_name):
    file_path = os.path.join(folder_name, file_name)
    file_path = file_path[:255]
    if os.path.exists(file_path):
        print("file lock acquisition: failed for: %s" % file_path)
        return False
    print("file lock acquisition: attempted for: %s" % file_path)
    os.mknod(file_path)
    print("file lock acquisition: acquired for: %s" % file_path)
    return True

def _clear_wiktionary_file_locks(lock_folder="wiktionary-locks"):
    for file in os.listdir(lock_folder):
        os.remove(os.path.join(lock_folder, file))

# Use scrapy to parse the wiktionary url (TODO MAKE THIS COMMENT MORE COMPLETE)
def _parse_wiktionary(wiktionary_url, word, part_of_speech, use_cache=False):
    global parse_wiktionary_lock
    output_file_path = "definition-cache/scrapy-scrape-test--%s-%s.json"\
        % (word, part_of_speech)
    if not use_cache or not os.path.exists(output_file_path):
        lock_folder_name = "wiktionary-locks"
        lock_file_name = "%s-%s" % (word, part_of_speech)
        lock_file_name = lock_file_name.replace("/", "-slash-")
        parse_wiktionary_lock.acquire()
        print("parse_wiktionary_lock: acquired")
        lock_acquired = _try_acquire_file_lock(lock_folder_name, lock_file_name)
        parse_wiktionary_lock.release()
        print("parse_wiktionary_lock: released")
        if lock_acquired:
            print("file lock acquired, running scrapyd.....")
            _run_scrapyd_spider(
                wiktionary_url, word, part_of_speech, output_file_path)
            parse_wiktionary_lock.acquire()
            print("parse_wiktionary_lock: acquired")
            os.remove(os.path.join(lock_folder_name, lock_file_name))
            print("file lock acquisition: released for: %s" % lock_file_name)
            parse_wiktionary_lock.release()
            print("parse_wiktionary_lock: released")
        else:
            while not os.path.exists(output_file_path):
                time.sleep(1)

    print("\n\n\n")
    if not os.path.exists(output_file_path):
        return ""
    with open(output_file_path, 'r') as json_definition_data:
        try:
            definition_data = json.load(json_definition_data)
            print("definition_data: %s" % definition_data)
        except:
            print("ERROR: Could not find definition file at path: %s" 
                % output_file_path)
            return ""
    return definition_data[0]['definition']

def _run_scrapyd_spider(urls, word, part_of_speech, output_file_path):
    spider_file = "sentence_graph_prototype.py"
    if not isinstance(urls, types.ListType):
        urls = [urls]
    print(
        "Running scrapyd spider with word: %s part of speech: %s and url: %s" 
            % (word, part_of_speech, urls))
    print(
        "Command used: scrapy runspider %s -a urls=%s -a word=%s -a part_of_speech=%s -a output_file_path=%s" 
            % (spider_file, ",".join(urls), word, part_of_speech, output_file_path))
    subprocess.check_call([
        "scrapy", 
        "runspider", 
        spider_file, 
        "-a",
        "urls=%s" % ",".join(urls),
        "-a",
        "word=%s" % word,
        "-a",
        "part_of_speech=%s" % part_of_speech,
        "-a",
        "output_file_path=%s" % output_file_path])

################################################################################
###################-----Sentence Graph Building Functions-----##################
################################################################################

# Takes some body of text, splits it into sentences, constructs sentence
# graphs for every sentence, and returns a list of all the sentence graphs.
def get_text_sentence_graphs(text, directed=False):
    sentence_graphs = []
    for sentence in text.split("."):
        if sentence.strip() == "":
            continue
        sentence_graphs.append(build_deep_sentence_graph(sentence))
    return sentence_graphs


# Take a string sentence and recursively build a sentence graph by looking up 
# the definition of each word and adding an edge from each word to the graph of 
# the sentence defining the word. Perform this process recursively and if a word
# that already exists in the graph is encountered then add an edge to that 
# pre-existing word instead of diving deep again.
#
# Eventually this process should stop....
# If it proves unreasonably long-running, then set a depth limit or something 
# similar
#
# Return the deep sentence graph
def build_deep_sentence_graph(
        sentence,
        definition_provider=lookup_definition_on_wiktionary, 
        directed=False,
        depth=10):
    sentence_graph = Graph(directed=directed)
    
    # Vertex properties
    word_property = sentence_graph.new_vertex_property("string")
    part_of_speech_property = sentence_graph.new_vertex_property("string")
    word_pos_tuple_property = sentence_graph.new_vertex_property("object")
    vertex_color_property = sentence_graph.new_vertex_property("vector<double>")
    sentence_graph.vertex_properties["word"] = word_property
    sentence_graph.vertex_properties["part_of_speech"] = part_of_speech_property
    sentence_graph.vertex_properties["word_pos_tuple"] = word_pos_tuple_property
    sentence_graph.vertex_properties["vertex_color"] = vertex_color_property

    # Edge properties
    sentence_edge_property = sentence_graph.new_edge_property("string")
    definition_edge_property = sentence_graph.new_edge_property("string")
    sentence_graph.edge_properties["sentence_edge"] = sentence_edge_property
    sentence_graph.edge_properties["definition_edge"] = definition_edge_property

    word_pos_to_vertex_index_mapping = dict()

    first_sentence_vertices = _build_deep_sentence_graph_helper(
        sentence, 
        sentence_graph, 
        word_pos_to_vertex_index_mapping,
        definition_provider,
        directed,
        depth=depth)

    print("Setting base sentence coloring.....")
    for word_vertex in first_sentence_vertices:
        print("Processing word_vertex: %s" % 
            sentence_graph.vertex_properties["word"][word_vertex])
        sentence_graph.vertex_properties["vertex_color"][word_vertex] =\
            [1, 0, 0, 1]

    return sentence_graph

def _build_deep_sentence_graph_helper(
        sentence,
        sentence_graph,
        word_pos_to_vertex_index_mapping,
        definition_provider, 
        directed,
        depth=None):
    if depth is not None:
        if depth == 0:
            return []
        depth -= 1

    print("DEBUG*****: Building deep sentence graph on sentence: %s" % sentence)
    sentence = sentence.replace(".", "").lower().strip()
    sentence_vertices = []
    # Parse with ParseyMcParseface to obtain parts of speech tagging
    sentence_parse_tree = parse_ascii_tree(run_parsey(sentence))
    if sentence_parse_tree is None:
        print(
            "\n\nERROR: sentence_parse_tree from parse_ascii_tree is None for"
            " sentence:\n %s\n\n" % sentence)
        return []

    prev_word_vertex = None
    for parse_node in sentence_parse_tree.to_sentence_order():
        word = parse_node.word
        try:
            part_of_speech =\
                PARSEY_PART_OF_SPEECH_TO_WIKTIONARY_MAP[parse_node.part_of_speech]
        except:
            continue

        word_pos_tuple = (word, part_of_speech)
        if word_pos_tuple in word_pos_to_vertex_index_mapping:
            # Set word_vertex to the previously found vertex
            word_vertex_index = word_pos_to_vertex_index_mapping[word_pos_tuple]
            word_vertex = sentence_graph.vertex(word_vertex_index)
        else:
            # Create vertex, set properties
            word_vertex = sentence_graph.add_vertex()
            sentence_graph.vertex_properties["word"][word_vertex] = word
            sentence_graph.vertex_properties["part_of_speech"][word_vertex] =\
                part_of_speech
            sentence_graph.vertex_properties["word_pos_tuple"][word_vertex] =\
                word_pos_tuple
            sentence_graph.vertex_properties["vertex_color"][word_vertex] =\
                [0, 0, 1, 1]
            word_pos_to_vertex_index_mapping[word_pos_tuple] =\
                sentence_graph.vertex_index[word_vertex]

            # Get definition, add pointer from word to all words in definition
            definition = definition_provider(word, part_of_speech)

            if definition.strip() != '':
                # Get definition of definitions
                definition_word_vertices = _build_deep_sentence_graph_helper(
                    definition,
                    sentence_graph, 
                    word_pos_to_vertex_index_mapping,
                    definition_provider=definition_provider, 
                    directed=directed,
                    depth=depth)

                # Add edges from the word_vertex to all definition vertices and set 
                # the definition edge property on each edge
                for definition_word_vertex in definition_word_vertices:
                    definition_edge = sentence_graph.add_edge(
                        word_vertex, definition_word_vertex)
                    sentence_graph.edge_properties["definition_edge"][definition_edge] =\
                        definition_edge
            else:
                print("\n\nERROR: definition not found for:\nword: %s\n"
                    "part of speech:%s\n\n\n" % (word, part_of_speech))
                open("failed-definition-lookups/%s-%s" % (word, part_of_speech), 'w')
                    .write("word: %s\npart of speech:%s\n", % (word, part_of_speech))
                    .close()

        sentence_vertices.append(word_vertex)

        # Add sentence edge and set sentence edge property on edge
        if prev_word_vertex is not None:
            sentence_edge = sentence_graph.add_edge(
                prev_word_vertex, word_vertex)
            sentence_graph.edge_properties["sentence_edge"][sentence_edge] =\
                sentence_edge
        prev_word_vertex = word_vertex

    return sentence_vertices

# Take a sentence in some form and generate a graph
# edges are built up using word order
#
# Return graph of sentence
def generate_linear_sentence_graph(sentence, directed=False):
    words = sentence.split(" ")
    
    sentence_graph = Graph(directed=directed)
    word_vertices = sentence_graph.add_vertex(len(words))
    word_property = sentence_graph.new_vertex_property("string")
    sentence_graph.vertex_properties["word"] = word_property
    for word_vertex, word in zip(word_vertices, words):
        word_property[word_vertex] = word
    sentence_graph.add_edge_list([(i - 1, i) for i in range(1, len(words))])

    sentence_graph_draw(
        sentence_graph, sentence, "linear-sentence-graph-debug.png")

# Takes a list of sentence graphs, finds the common vertices between them and
# returns a list of copies of the sentence graphs with all the common vertices 
# removed, with the exception of sentence vertices that are part of the base 
# sentence that the sentence graph was constructed from
def reduce_sentence_graphs(sentence_graphs, reduction_threshold=0.7):
    sentence_graph_words = dict(
        get_word_pos_tuples_from_sentence_graph(sentence_graphs[0]))
    for sentence_graph in sentence_graphs:
            for word_pos_count_tuple in get_word_pos_tuples_from_sentence_graph(sentence_graph):
                if word_pos_count_tuple[0] in sentence_graph_words:
                    sentence_graph_words[word_pos_count_tuple[0]] += 1

    for word_pos_tuple in sentence_graph_words.keys():
        if sentence_graph_words[word_pos_tuple] / len(sentence_graphs) <= 0.7:
            del sentence_graph_words[word_pos_tuple]

    reduced_sentence_graphs = []
    for sentence_graph in sentence_graphs:
        reduced_sentence_graph = sentence_graph.copy()
        
        for vertex in sentence_graph.vertices():
            word =\
                reduced_sentence_graph.vertex_properties["word"][vertex]
            part_of_speech =\
                reduced_sentence_graph.vertex_properties["part_of_speech"][vertex]
            # TODO: don't remove sentence vertices
            if (word, part_of_speech) in sentence_graph_words:
                # TODO: Remove the vertices, after verifying when it is useful, maybe make this a parameter
                # reduced_sentence_graph.remove_vertex(vertex)
                sentence_graph.vertex_properties["vertex_color"][vertex] =\
                    [1, 1, 0, 0]

        reduced_sentence_graphs.append(reduced_sentence_graph)


    return reduced_sentence_graphs

def get_word_pos_tuples_from_sentence_graph(sentence_graph):
    return [((sentence_graph.vertex_properties["word"][x], 
        sentence_graph.vertex_properties["part_of_speech"][x]), 1)
            for x in sentence_graph.vertices()]

# Draw the passed in sentence graph # TODO: make this comment more descriptive
def sentence_graph_draw(
        sentence_graph, 
        sentence,
        output_folder_name="sentence-graphs-visualization",
        output_file_name="sentence-graph-debug",
        file_extension=".png"):
    base_vertex_font_size = 128
    base_vertex_size = 200
    print("sentence_graph_draw for sentence: %s" % sentence)
    print("Words in sentence graph: %s" 
        % sentence_graph.vertex_properties["word"])
    if len([x for x in sentence_graph.vertices()]) == 0:
        print("Empty sentence graph received, cannot draw, returning....")
        return
    max_in_degree = max(
        [vertex for vertex in sentence_graph.vertices()], 
        key=lambda x: x.in_degree()).in_degree()
    print("Max in degree in sentence graph is: %s" % str(max_in_degree))
    font_size_func =\
        lambda in_degree: min(128, max(32, (in_degree / max(1, max_in_degree))))

    vertex_font_size_property_map = sentence_graph.degree_property_map("in")
    for key in sentence_graph.vertices():
        vertex_font_size_property_map[key] =\
            font_size_func(vertex_font_size_property_map[key])
    vertex_size_property_map = sentence_graph.degree_property_map("in")
    for key in sentence_graph.vertices():
        vertex_size_property_map[key] =\
            base_vertex_size *\
                (vertex_size_property_map[key] / max(1, max_in_degree))

    output_file_name = output_file_name.replace("/", "-slash-")
    output_file_path = os.path.join(output_folder_name, output_file_name)
    shortened_output_file_path = output_file_path[:252]

    graph_draw(
        sentence_graph, 
        vertex_text=sentence_graph.vertex_properties["word"], 
        vertex_font_size=vertex_font_size_property_map,
        vertex_fill_color=sentence_graph.vertex_properties["vertex_color"],
        output_size=(20000, 20000), 
        output=shortened_output_file_path + file_extension)
    
def sentence_graph_file_path_from_sentence(
    sentence, 
    sentence_graphs_folder="sentence-graphs-storage",
    file_extension=".gt"):
    sentence = sentence.replace(" ", "-")
    sentence = sentence.replace("/", "-slash-")
    file_path = os.path.join(sentence_graphs_folder, sentence)
    shortened_file_path = file_path[:252]
    print("Returning sentence_graph_file_path_from_sentence as: %s" 
        % (shortened_file_path + file_extension))
    return shortened_file_path + file_extension

def save_sentence_graph_to_file(
        sentence_graph, output_file_path, file_format="gt"):
    sentence_graph.save(
        output_file_path,
        fmt=file_format)

def load_sentence_graph_from_file(input_file_path, file_format="gt"):
    try:
        return load_graph(input_file_path, fmt=file_format)
    except:
        return None


################################################################################
##################-----Sentence Graph Operation Functions-----##################
################################################################################

# Compute a similarity score between 0.0-1.0 between two passed in graphs
def compute_graph_similarity_score(graph1, graph2):
    pass

################################################################################
##############################-----Test & Main-----#############################
################################################################################

def sentence_graph_test(sentence, graphic_output_file_name, depth=2):
    print("Testing build_deep_sentence_graph with sentence_graph_draw....")
    sentence_graph = build_deep_sentence_graph(
        sentence, directed=True, depth=depth)
    sentence_graph_draw(
        sentence_graph,
        sentence,
        output_file_name=graphic_output_file_name)
    save_sentence_graph_to_file(
        sentence_graph, sentence_graph_file_path_from_sentence(sentence))
    loaded_sentence_graph = load_sentence_graph_from_file(
        sentence_graph_file_path_from_sentence(sentence))
    if topology.isomorphism(sentence_graph, loaded_sentence_graph):
        print("Sentence graph successfully loaded from file!!!!")
    else:
        print("Sentence graph saved and loaded from file was corrupted!")

    return sentence_graph

def print_reduction_statistics(
        sentence, sentence_graph, reduced_sentence_graph):
    print("Sentence: %s" % sentence)
    print("Vertices in original graph: %d" 
        % len([x for x in sentence_graph.vertices()]))
    print("Vertices in reduced graph: %d" 
        % len([x for x in reduced_sentence_graph.vertices()]))

def scrapy_test():
    global DEBUG_iteration_number
    for i in range(50):
        print("Iteration: %d" % i)
        DEBUG_iteration_number = i
        _parse_wiktionary(
            WIKTIONARY_WEB_ROOT_URL, "plethora", "noun", use_cache=False)
        

#################################################### Multiprocessing function

def sentence_graph_creation_func(sentence):
    global shared_sentence_graphs_list
    global shared_sentence_graph_count
    print("Creating sentence graph for sentence: %s" % sentence)
    loaded_from_file = True
    depth = 1
    directed = True

    sentence = sentence.strip()
    sentence_graph = load_sentence_graph_from_file(
            sentence_graph_file_path_from_sentence(sentence))
    if sentence_graph is None:
        sentence_graph =\
            build_deep_sentence_graph(
                sentence, directed=directed, depth=depth)
        loaded_from_file = False

    shared_sentence_graphs_list.append(sentence_graph)
    shared_sentence_graph_count.set(shared_sentence_graph_count.get() + 1)

    if not loaded_from_file:
        # Save sentence graphs
        save_sentence_graph_to_file(
            sentence_graph, 
            sentence_graph_file_path_from_sentence(sentence))

    sentence_graph_draw(
        sentence_graph,
        sentence,
        output_folder_name="sentence-graphs-visualization/",
        output_file_name="reductions-test--%s----PRE_REDUCTION.png"\
            % sentence.replace(" ", "-"))

    return sentence_graph

def test():
    global DEBUG_restart_sentence_index

    """
    print("Grabbing article text for Graph-Tool......\n")
    print(\
        _strip_wikipedia_citations(\
            get_article_text(\
                "https://en.wikipedia.org/wiki/Graph-tool")))

    print("\n\n\n")

    print("Printing 500 wikipedia article URLs.......\n")
    print("".join([x for x in itertools.islice(get_all_wikipedia_urls(\
        WIKIPEDIA_WEB_ROOT_URL, WIKIPEDIA_ARTICLE_LIST_FILE_PATH), 500)]))

    print("\n\n\n")

    print("Scraping 5 wikipedia pages.......\n")
    for wikipedia_scrape in scrape_wikipedia():
        print("\n\n\n\n")
        print("Wikipedia Scrape:")
        print(wikipedia_scrape)
    
    print("\n\n\n")

    print("Scraping wiktionary pages.......\n")
    print("lookup_definition_on_wiktionary(police, noun): %s" 
        % lookup_definition_on_wiktionary("police", "noun"))
    print("\n")
    
    print("\n\n\n")

    generate_linear_sentence_graph("This is a sentence and it is great")
    
    print("\n\n\n")

    print("Testing run_parsey....")
    print("run_parsey(): ||%s||" % run_parsey("this here is a sentence, it is nice."))
    """

    """
    print("\n\n\n")

    print("Testing scrapyd spider")
    print("Output: %s" % _run_scrapyd_spider(
        "https://en.wiktionary.org/wiki/dogs",
        "dogs",
        "noun",
        "~/tester.json"))

    print("\n\n\n")    
    """

    """
    depth = 4
    sentence_graph_1 = sentence_graph_test(
        "Donald Trump is a tyrannical ruler", 
        "donald-trump-1--synonym-sentence-graphs-debug--depth-%s.png" % depth,
        depth=depth)
    sentence_graph_2 = sentence_graph_test(
        "Donald Trump is a despotic ruler", 
        "donald-trump-2--synonym-sentence-graphs-debug--depth-%s.png" % depth,
        depth=depth)
    if topology.isomorphism(sentence_graph_1, sentence_graph_2):
        print("That was easy, those sentence graphs are the same!")
    else:
        print("As expected, it isn't that easy, the sentence graphs differ.")
    """

    """
    depth = 4
    sentence_graph_1 = sentence_graph_test(
        "tyrannical", 
        "synonyms-tyrannical--synonym-sentence-graphs-debug--depth-%s.png" % depth,
        depth=depth)
    sentence_graph_2 = sentence_graph_test(
        "despotic", 
        "synonyms-despotic--synonym-sentence-graphs-debug--depth-%s.png" % depth,
        depth=depth)
    if topology.isomorphism(sentence_graph_1, sentence_graph_2):
        print("That was easy, those sentence graphs are the same!")
    else:
        print("As expected, it isn't that easy, the sentence graphs differ.")
    """

    """
    tyrannical_sentence_graph = load_sentence_graph_from_file(
        "sentence-graphs-storage/tyrannical.gt")
    despotic_sentence_graph = load_sentence_graph_from_file(
        "sentence-graphs-storage/despotic.gt")

    tyrannical_words = [tyrannical_sentence_graph.vertex_properties["word"][x] 
            for x in tyrannical_sentence_graph.vertices()]
    print("words in tyrannical sentence graph: %s" % tyrannical_words)
    print("\n\n\n")

    despotic_words = [despotic_sentence_graph.vertex_properties["word"][x] 
            for x in despotic_sentence_graph.vertices()]
    print("words in despotic sentence graph: %s" % despotic_words)

    print("\n\n")
    shared_words = list(set(tyrannical_words) & set(despotic_words))
    print("Shared words: %s" % shared_words)

    print("\n\nNumber of tyrannical words: %d" % len(tyrannical_words))
    print("Number of despotic words: %d" % len(despotic_words))
    print("Number of shared words: %d" % len(shared_words))
    print("Number of unique tyranical words: %d" 
        % (len(tyrannical_words) - len(shared_words)))
    print("Number of unique despotic words: %d" 
        % (len(despotic_words) - len(shared_words)))
    """

    """
    print("\n\n\n")
    sentences = [
        "The medical procedure went as planned",
        "War is hell",
        "America's new ruler is a fascist",
        "Hiking is a fun activity",
        "Space is the final frontier",
        "The bacteria in this sample are growing at an accelerated rate",
        "This graph is enormous",
        "Linear algebra is a study of matrices",
        "I need a haircut",
        "The code was broken",
    ]

    depth = 3
    sentence_graphs = []
    output_folder_name="sentence-graphs-storage"
    loaded_from_file = True
    print("Drawing base sentence graphs:")
    for sentence in sentences:
        sentence_graph = load_sentence_graph_from_file(
                sentence_graph_file_path_from_sentence(sentence))
        if sentence_graph is None:
            sentence_graph =\ 
                build_deep_sentence_graph(sentence, directed=True, depth=depth)
            loaded_from_file = False

        sentence_graph_draw(
            sentence_graph,
            sentence,
            output_folder_name="sentence-graphs-visualization/",
            output_file_name="reductions-test--%s----PRE_REDUCTION.png"\
                % sentence.replace(" ", "-"))

        sentence_graphs.append(sentence_graph)

    if not loaded_from_file:
        # Save sentence graphs
        for sentence, sentence_graph in zip(sentences, sentence_graphs):
            save_sentence_graph_to_file(
                sentence_graph, 
                sentence_graph_file_path_from_sentence(sentence))

    reduced_sentence_graphs = reduce_sentence_graphs(sentence_graphs)
    print("\nDrawing reduced sentence graphs")
    for i in range(len(sentences)):
        print_reduction_statistics(
            sentences[i], sentence_graphs[i], reduced_sentence_graphs[i])
        sentence_graph_draw(
            sentence_graphs[i],
            sentences[i],
            output_folder_name="sentence-graphs-visualization/",
            output_file_name="reductions-test--%s.png"\
                % sentences[i].replace(" ", "-"))
    """


    
    #"""
    print("\n\n\n")
    _clear_wiktionary_file_locks()
    sentences = BBC_ARTICLE.split('.')
    sentences = filter(lambda x: x.strip() != '', sentences)

    #sentence_graphs = pool.map(sentence_graph_creation_func, sentences, 1)

    DEBUG_restart_sentence_index = 0 # 430
    sentence_graphs = []
    for i in range(DEBUG_restart_sentence_index, len(sentences)):
        print("DEBUG_restart_sentence_index: %d" % i)
        sentence = sentences[i]
        try:
            sentence_graphs.append(sentence_graph_creation_func(sentence))
        except Exception:
            exception_type, exception_value, exception_traceback = sys.exc_info()
            print("DEBUG_restart_sentence_index: %d" % i)
            raise exception_type, exception_value, exception_traceback
        DEBUG_restart_sentence_index += 1

    print("Closing pool.....")
    pool.close()
    print("Processed %s sentences" % str(shared_sentence_graph_count))

    print("Reducing sentence graphs.....")
    reduced_sentence_graphs = reduce_sentence_graphs(sentence_graphs)
    print("Reduced %d sentence graphs" % len(reduced_sentence_graphs))
    print("\nDrawing reduced sentence graphs.....")
    for i in range(len(sentence_graphs)):
        print_reduction_statistics(
            sentences[i], sentence_graphs[i], reduced_sentence_graphs[i])
        sentence_graph_draw(
            sentence_graphs[i],
            sentences[i],
            output_folder_name="sentence-graphs-visualization/",
            output_file_name="reductions-test--%s.png"\
                % sentences[i].replace(" ", "-"))
    print("Drew %d reduced sentence graphs" % len(sentences))
    #"""

if __name__ == '__main__':
    test()