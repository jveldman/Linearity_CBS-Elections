# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 11:23:24 2022

@author: jjhve
"""
import json
# script for defining relive units
# already relative
rela_age = ['JongerDan5Jaar_13', 'k_5Tot10Jaar_14' , 'k_10Tot15Jaar_15', 'k_15Tot20Jaar_16','k_20Tot25Jaar_17',  'k_25Tot45Jaar_18', 
            'k_45Tot65Jaar_19', 'k_65Tot80Jaar_20','k_80JaarOfOuder_21']
# Already relative to totale druk. tov productieve leeftijdsgroep 20-65
rela_press = ['GroeneDruk_23', 'GrijzeDruk_24']
# Already relative to amount of people of 15 years and older
rela_huw = ['Ongehuwd_30', 'Gehuwd_31', 'Gescheiden_32', 'Verweduwd_33']
# Already relative to percentage of inhabitants per 1 januari
rela_immi = ['NederlandseAchtergrond_43', 'TotaalMetMigratieachtergrond_44', 'WesterseMigratieachtergrond_45', 
             'TotaalNietWesterseMigratieachtergrond_46', 'Marokko_47','VoormaligeNederlandseAntillenAruba_48', 
             'Suriname_49', 'Turkije_50', 'OverigNietWesterseMigratieachtergrond_51']
# Still to divide by TotaleBevolking_1
rela_urban = {'TotaleBevolking_1':['ZeerSterkStedelijk_52', 'SterkStedelijk_53', 
                                   'MatigStedelijk_54', 'WeinigStedelijk_55', 'NietStedelijk_56']}
# Already rela
rela_density = ['Bevolkingsdichtheid_57']
#
rela_birthmort = ['GeboorteRelatief_59', 'SterfteRelatief_61', 'GeboorteoverschotRelatief_63']
# To divide by TotaleBevolking_1
rela_desease = {'TotaleBevolking_1':['Nieuwvormingen_64','ZiektenVanHartEnVaatstelsel_65','ZiektenVanAdemhalingsstelsel_66', 'UitwendigeDoodsoorzaken_67', 
                'OverigeDoodsoorzaken_68']}
# already rela
rela_migration = ['BinnenlandsMigratiesaldoRelatief_72', 'VerhuismobiliteitRelatief_73','MigratiesaldoRelatief_77', 'BevolkingsgroeiRelatief_80']
# Already rela. Average household size is already standardised per household
rela_househ = ['Eenpersoonshuishoudens_86', 'HuishoudensZonderKinderen_87','HuishoudensMetKinderen_88', 'GemiddeldeHuishoudensgrootte_89']
rela_houses = ['SaldoVermeerderingWoningenRelatief_92','Woningdichtheid_93', 'Koopwoningen_94', 'Huurwoningen_95','EigendomOnbekend_96']
# rela onderwijs, make relative to TotaleBevolking_1. 
# make relative to total population.
rela_primary = {'TotaleBevolking_1':['SpeciaalBasisonderwijs_101','SpecialeScholen_102']}
# make relative to total population
rela_highs = {'TotaleBevolking_1':['VoortgezetOnderwijs_103']}
#Rela_study both to total amount of students and total population
rela_study = {'TotaleBevolking_1':['BeroepsopleidendeLeerweg_104', 'BeroepsbegeleidendeLeerweg_105', 'HogerBeroepsonderwijs_106', 'WetenschappelijkOnderwijs_107']}
# to didive by TotaleBevolking_1
rela_finstudy = {'TotaleBevolking_1':['VoortgezetOnderwijs_108', 'MiddelbaarBeroepsonderwijs_109','HogerBeroepsonderwijsBachelor_110', 'WoMasterDoctoraal_111']}
# already relative to total amount of jobs 
rela_job = ['ALandbouwBosbouwEnVisserij_117', 'BFNijverheidEnEnergie_118', 'GNCommercieleDienstverlening_119','OUNietCommercieleDienstverlening_120']
# spendable income, since it's average of a specific type of household, averaging is not necessary
spend_inc = ['ParticuliereHuishoudensExclStudenten_132','TypeEenpersoonshuishouden_133', 'TypeEenoudergezin_134', 'TypePaarZonderKind_135', 
             'TypePaarMetKindEren_136', 'BronInkomenAlsWerknemer_137', 'BronInkomenAlsZelfstandige_138', 
             'BronOverdrachtsinkomen_139', 'WoningbezitEigenWoning_140', 'WoningbezitHuurwoning_141']
spend_incmed = ['ParticuliereHuishoudensExclStudenten_142','TypeEenpersoonshuishouden_143', 'TypeEenoudergezin_144', 'TypePaarZonderKind_145', 
             'TypePaarMetKindEren_146', 'BronInkomenAlsWerknemer_147', 'BronInkomenAlsZelfstandige_148', 
             'BronOverdrachtsinkomen_149', 'WoningbezitEigenWoning_150', 'WoningbezitHuurwoning_151']
# to divide by TotaleBevolking_1
rela_welfare = {'TotaleBevolking_1':['UitkeringsontvangersTotaal_152', 'TotDeAOWLeeftijd_153', 'VanafDeAOWLeeftijd_154', 'Werkloosheid_155',
                'BijstandGerelateerdTotAOWLeeftijd_156', 'BijstandGerelateerdVanafAOWLeeftijd_157', 'BijstandTotDeAOWLeeftijd_158', 
                'ArbeidsongeschiktheidTotaal_159','WAOUitkering_160', 'WIAUitkeringWGARegeling_161', 'WajongUitkering_162', 
                'AOW_163']}
# to divide by BedrijfsvestigingenTotaal_164
rela_business= {'BedrijfsvestigingenTotaal_164':['ALandbouwBosbouwEnVisserij_165', 'BFNijverheidEnEnergie_166', 
                                                 'GIHandelEnHoreca_167', 'HJVervoerInformatieEnCommunicatie_168', 
                                                 'KLFinancieleDienstenOnroerendGoed_169', 'MNZakelijkeDienstverlening_170', 'RUCultuurRecreatieOverigeDiensten_171']}
# Already percentage of TotaleOppervlakte_183
rela_farm = {'TotaleOppervlakte_183':['Akkerbouw_184', 'TuinbouwOpenGrond_185', 'TuinbouwOnderGlas_186','BlijvendGrasland_187', 'NatuurlijkGrasland_188', 
             'TijdelijkGrasland_189', 'Groenvoedergewassen_190']}
# already per 1000 inhabitants
rela_transport = ['PersonenautoSRelatief_197', 'PersonenautoSParticulierenRelatief_199', 'MotorfietsenRelatief_202', 'VoertuigenMetBromfietskenteken_204']
# Living stats, distance is in kilometers and quantity is within 3 or 20 km
rela_distance = ['AfstandTotHuisartsenpraktijk_209','AantalHuisartsenpraktijkenBinnen3Km_210', 'AfstandTotHuisartsenpost_211', 
                 'AfstandTotZiekenhuis_212', 'AantalZiekenhuizenBinnen20Km_213', 'AfstandTotKinderdagverblijf_214', 'AantalKinderdagverblijvenBinnen3Km_215', 
                 'AfstandTotSchoolBasisonderwijs_216', 'AantalBasisonderwijsscholenBinnen3Km_217', 'AfstandTotSchoolVmbo_218', 
                 'AantalScholenVmboBinnen5Km_219', 'AfstandTotSchoolHavoVwo_220', 'AantalScholenHavoVwoBinnen5Km_221', 'AfstandTotGroteSupermarkt_222', 
                 'AantalGroteSupermarktenBinnen3Km_223', 'AfstandTotRestaurant_224', 'AantalRestaurantsBinnen3Km_225', 'AfstandTotBibliotheek_226', 
                 'AfstandTotBioscoop_227', 'AantalBioscopenBinnen10Km_228', 'AfstandTotZwembad_229','AfstandTotSportterrein_230', 
                 'AfstandTotOpenbaarGroen_231', 'AfstandTotOpritHoofdverkeersweg_232',  'AfstandTotTreinstation_233']
# litter, still to divide by TotaalHuishoudelijkAfval_234
rela_litter = {'TotaalHuishoudelijkAfval_234':['HuishoudelijkRestafval_235', 'GrofHuishoudelijkRestafval_236', 'GftAfval_237', 'OudPapierEnKarton_238', 
               'Verpakkingsglas_239', 'Textiel_240', 'KleinChemischAfval_241', 'OverigHuishoudelijkAfval_242' ]}
# land usage, already relative
rela_land = ['Verkeersterrein_255', 'BebouwdTerrein_256', 'SemiBebouwdTerrein_257','Recreatieterrein_258', 'AgrarischTerrein_259', 
             'BosEnOpenNatuurlijkTerrein_260']
# land ha per 1000 inhabitants
rela_landpi = ['Verkeersterrein_261','BebouwdTerrein_262', 'SemiBebouwdTerrein_263', 'Recreatieterrein_264','AgrarischTerrein_265', 
               'BosEnOpenNatuurlijkTerrein_266']

completelist = [rela_age, rela_birthmort, rela_business, rela_density, rela_desease, rela_distance, rela_farm, 
                rela_finstudy, rela_highs, rela_househ, rela_houses, rela_huw, rela_immi, rela_job, rela_land, 
                rela_landpi, rela_litter, rela_migration, rela_press, rela_primary, rela_study, 
                rela_transport, rela_urban, rela_welfare, spend_inc, spend_incmed]

def save_json(location, file): 
    string = json.dumps(file)
    jsonFile = open(location, "w")
    jsonFile.write(string)
    jsonFile.close()

save_json('C:/Users/jjhve/Documents/TilburgUniversity/PolProj/itertable.json',completelist)