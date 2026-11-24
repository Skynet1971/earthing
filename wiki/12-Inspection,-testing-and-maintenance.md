> Earthing, Bonding, Surge & Lightning Protection Library · **SHEET 12 · TESTING** · content version 1.0

# Inspection, testing and maintenance

*Inspection intervals, continuity values, earth electrode measurement, inspection after a strike, SPD end of life, PV insulation tests and who may do the work*

**Applies to:** Earthing and bonding systems, earth electrodes, lightning protection systems, surge protective devices, RCDs and PV arrays of a house and its outbuildings

📄 **PDF:** [12_inspection_testing_maintenance.pdf](https://github.com/Skynet1971/earthing/raw/HEAD/docs/pdf/12_inspection_testing_maintenance.pdf)

> ℹ️ Information only. Every technical statement cites a source and PDF page; it does not replace the wiring code that applies at the site, the product manuals, or a qualified and registered person.

## 1  Who may do the work

DEHN states that inspection of a lightning protection system must be carried out by a lightning protection specialist.<sup>[R6 p.56](#sources-cited-on-this-page)</sup>

- Per the South African WAPA high-site guideline, earthing systems must comply with SANS 10142-1 (wiring of premises, low-voltage installations) and be carried out and certified by competent registered persons.<sup>[R13 p.20](#sources-cited-on-this-page)</sup>
- Per the South African WAPA high-site guideline, LPS design is complex, needs specialist knowledge and LPS and earthing specialists should be consulted.<sup>[R13 p.21](#sources-cited-on-this-page)</sup>
- Per the German standard DIN 18014, installing a foundation earth electrode is an electrical measure that must be carried out or supervised by a certified lightning protection specialist or electrician.<sup>[R6 p.131](#sources-cited-on-this-page)</sup>
- Per US DoD guide spec UFGS 27 05 26, the bond between the AC equipment ground (ACEG) and the PBB or SBB must be installed by a licensed electrician.<sup>[R17 p.10](#sources-cited-on-this-page)</sup>
- SMA technical information (Overvoltage Protection, v1.3): an expert on lightning protection must determine for each PV system which lightning and overvoltage protection measures are necessary.<sup>[R45 p.1](#sources-cited-on-this-page)</sup>
- Sunsynk 8 kW hybrid inverter manual: WARNING - high life risk due to fire or electrocution; the inverter can only be installed by a qualified licensed electrical contractor and is not a DIY product.<sup>[R46 p.6](#sources-cited-on-this-page)</sup>
- Centurion (D5-Evo sliding gate operator installation manual): all electrical work must follow applicable local electrical codes, and a licensed electrical contractor is recommended.<sup>[R33 p.31](#sources-cited-on-this-page)</sup>
- Per NIST (US), fitting a snap-in panel surge protector means removing the panel front with the main breaker turned off; the homeowner should check whether local authorities allow them to do it, or hire a licensed electrician.<sup>[R1 p.10](#sources-cited-on-this-page)</sup>
- Siemens LOGO! 8 system manual: only qualified personnel who are familiar with and follow general engineering rules and the relevant regulations and standards may install LOGO! devices.<sup>[R28 p.31](#sources-cited-on-this-page)</sup>
- SAPVIA PV guidelines (South Africa, 2017): module interconnection with pre-fitted connectors can be done by a trained non-electrician under supervision of an electrically skilled person only while there are no exposed live parts; additional wiring and assembly of plugs must be performed by an electrician.<sup>[R47 p.28](#sources-cited-on-this-page)</sup>

> [!NOTE]
> **NOTE: Shock protection comes first**
>
> DEHN states that measures for protection against electric shock always take priority over surge protection measures.<sup>[R6 p.220](#sources-cited-on-this-page)</sup>

## 2  Safety before and during tests

> [!WARNING]
> **WARNING: Isolate before an earth electrode test, re-connect before energising**
>
> Per UK guidance (IEE Wiring Matters), the main switch-disconnector must be open before the measurement, because the installation is unprotected against earth faults during the test<sup>[R9 p.5](#sources-cited-on-this-page)</sup>; the means of earthing must be re-established before the installation is energised.<sup>[R9 p.5](#sources-cited-on-this-page)</sup>

- Centurion (D5-Evo sliding gate operator installation manual): before electrical work, check the circuit breaker is OFF and that all high voltage circuits (more than 42.4 V) are completely isolated from the mains supply.<sup>[R33 p.31](#sources-cited-on-this-page)</sup>
- Siemens LOGO! 8 system manual: power must always be switched off before wiring or installing/removing a module.<sup>[R28 p.31](#sources-cited-on-this-page)</sup>
- Sunsynk 8 kW hybrid inverter manual: because the system can still hold residual energy, wait 5 minutes after turning off the power before touching electrical components.<sup>[R46 p.6](#sources-cited-on-this-page)</sup>
- Per the South African WAPA high-site guideline, nobody should be allowed onto exposed areas of the site or to climb support structures when there is lightning, or lightning is expected, in the area.<sup>[R13 p.21](#sources-cited-on-this-page)</sup>
- Per UK guidance (IEE Wiring Matters), it is sensible to check the distributor's network map before driving earth rods.<sup>[R9 p.3](#sources-cited-on-this-page)</sup>
- ITU-T K.73 requires that where a cable screen is bonded at one end and left insulated at the other, the non-earthed end is protected against direct contact and labelled to warn of a potential electric shock risk.<sup>[R23 p.9](#sources-cited-on-this-page)</sup>

### PV arrays cannot be switched off

- BRE PV guide (UK, 2nd ed. 2006): the supply from PV modules cannot be switched off, so special precautions are needed to ensure live parts are not accessible or cannot be touched during installation, use and maintenance.<sup>[R49 p.5](#sources-cited-on-this-page)</sup>
- BRE PV guide (UK, 2nd ed. 2006): always test for the presence of voltage on parts before touching any part of the PV system.<sup>[R49 p.21](#sources-cited-on-this-page)</sup>
- BRE PV guide (UK, 2nd ed. 2006): an electric shock may be experienced from a capacitive discharge, because a charge may build up in the PV system due to its distributed capacitance to ground (more prevalent with thin-film modules with metal frames or steel backing).<sup>[R49 p.21](#sources-cited-on-this-page)</sup>
- BRE PV guide (UK, 2nd ed. 2006): an installer in contact with earthed metal (e.g. seated on an earthed metal roof) can get a shock to earth from PV cabling; insulated tools and gloves together with insulating matting to stand or sit on can mitigate this hazard.<sup>[R49 p.21](#sources-cited-on-this-page)</sup>
- BRE PV guide (UK, 2nd ed. 2006): an electric shock may also be experienced due to the PV array developing a ground leakage path, which good wiring practice, double insulation and Class II modules reduce but do not eliminate.<sup>[R49 p.22](#sources-cited-on-this-page)</sup>
- BRE PV guide (UK, 2nd ed. 2006): before an array insulation resistance test, any equipment that could affect the measurement, i.e. overvoltage protection (SPDs) in the junction or combiner boxes, must be disconnected.<sup>[R49 p.28](#sources-cited-on-this-page)</sup>

## 3  Inspection intervals

| Class of LPS | Visual inspection | Complete inspection | Complete inspection, critical situations |
|---|---|---|---|
| I and II | 1 year<sup>[R6 p.57](#sources-cited-on-this-page)</sup> | 2 years | 1 year |
| III and IV | 2 years<sup>[R6 p.57](#sources-cited-on-this-page)</sup> | 4 years | 1 year |

*Maximum periods between inspections per IEC 62305-3 Table E.2, as quoted by DEHN.<sup>[R6 p.57](#sources-cited-on-this-page)</sup>*

- A lightning protection system should also be inspected whenever it is known to have been struck by lightning, and after changes of use, modifications, extensions or repairs to the structure.<sup>[R6 p.57](#sources-cited-on-this-page)</sup>
- Per the South African WAPA high-site guideline, earth leakage protection devices should be tested once a year.<sup>[R13 p.30](#sources-cited-on-this-page)</sup>
- Per the South African WAPA high-site guideline, the earthing system should be checked once a year to confirm it is intact and its earth impedance has not risen unreasonably.<sup>[R13 p.30](#sources-cited-on-this-page)</sup>
- Per the South African WAPA high-site guideline, all earthing points and earth straps should be inspected once a year for damage, arcing or corrosion and repaired.<sup>[R13 p.30](#sources-cited-on-this-page)</sup>

### After a lightning strike

> [!TIP]
> **DO: Inspect after any strike or change to the building**
>
> DEHN: inspect the LPS whenever it is known to have been struck, and after changes of use, modifications, extensions or repairs to the structure.<sup>[R6 p.57](#sources-cited-on-this-page)</sup> WAPA (South Africa): immediately after lightning damage, inspect and repair all earthing points, earth straps and surge protection devices.<sup>[R13 p.30](#sources-cited-on-this-page)</sup>

## 4  Continuity of bonding and conductors

| **< 1 Ω** | **200 mA** | **100 mΩ** |
|---|---|---|
| continuity of air-terminations, down conductors, bonding and shielding, recommended value<sup>[R6 p.58](#sources-cited-on-this-page)</sup> | test current for bonding continuity tests per IEC 60364-6 (IEC 61557-4)<sup>[R6 p.180](#sources-cited-on-this-page)</sup> | telecom bonding system to building electrode system, US DoD (50 mΩ critical)<sup>[R17 p.33](#sources-cited-on-this-page)</sup> |

- In LPS inspections, the continuity of connections of air-terminations, down conductors, bonding conductors and shielding is measured; the recommended value is below 1 ohm.<sup>[R6 p.58](#sources-cited-on-this-page)</sup>
- A resistance of less than 1 ohm is considered sufficient for equipotential bonding connections when continuity is tested.<sup>[R6 p.180](#sources-cited-on-this-page)</sup>
- Continuity tests of bonding per IEC 60364-6 must use test equipment with a test current of 200 mA (IEC 61557-4).<sup>[R6 p.180](#sources-cited-on-this-page)</sup>
- Per US DoD guide spec UFGS 27 05 26, the recommended maximum resistance between any point of the telecommunications bonding system and the building grounding electrode system is 100 milliohms (50 milliohms for critical facilities).<sup>[R17 p.33](#sources-cited-on-this-page)</sup>
- Per US DoD guide spec UFGS 27 05 26, cable-tray bonding jumpers or manufacturer-supplied mechanical bonds must give a bonding resistance of at most 1 milliohm.<sup>[R17 p.18](#sources-cited-on-this-page)</sup>
- Per US DoD guide spec UFGS 27 05 26, ground-loop current is measured in the bonding conductors connected to the PBB/SBB with the grounding infrastructure complete and the electronics operating; the maximum acceptable AC current is 1 ampere.<sup>[R17 p.34](#sources-cited-on-this-page)</sup>
- ITU-T K.27: a single point connection in an isolated DC return system can be verified with a DC clamp-on ammeter around the connecting conductor; zero current confirms the single point connection.<sup>[R24 p.18](#sources-cited-on-this-page)</sup>

## 5  Earth electrode measurement

BS 7671:2001 Regulation 713-10-01 (UK) requires the resistance to earth of an earth electrode to be measured, before the installation is energised.<sup>[R9 p.4](#sources-cited-on-this-page)</sup>

- Per UK guidance (IEE Wiring Matters), the earth electrode test should ideally be done when ground conditions are least favourable, such as during dry weather, and it uses two temporary test electrodes (spikes).<sup>[R9 p.4](#sources-cited-on-this-page)</sup>
- Per UK guidance (IEE Wiring Matters), reliable earth electrode test results may be expected if the distance between the electrode under test and the current spike is at least ten times the maximum dimension of the electrode system, e.g. 30 m for a 3 m rod.<sup>[R9 p.4](#sources-cited-on-this-page)</sup>
- Per US DoD guide spec UFGS 27 05 26, the building grounding electrode system is tested by the three-point fall-of-potential method before the telecom bonding conductor is connected and must not exceed 25 ohms (5 ohms option), measured in dry weather not earlier than 48 hours after rain.<sup>[R17 p.33](#sources-cited-on-this-page)</sup>
- Per UK guidance (IEE Wiring Matters), at periodic inspection the earth electrode may be tested with an earth loop impedance tester, measuring between the phase conductor at the origin and the earth electrode with the test link open.<sup>[R9 p.5](#sources-cited-on-this-page)</sup>
- Per UK guidance (IEE Guidance Note 3 as cited by IEE Wiring Matters), in practice measured loop impedance values above 200 Ω will require further investigation.<sup>[R9 p.5](#sources-cited-on-this-page)</sup>
- Nemtek (Super Earthing Kit instruction manual): the bentonite backfill should cure for at least 24 hours before testing.<sup>[R32 p.2](#sources-cited-on-this-page)</sup>
- MikroTik tells installers to make sure the grounding infrastructure they connect to is fully functional and not merely decorative.<sup>[R21 p.1](#sources-cited-on-this-page)</sup>

> [!NOTE]
> **NOTE: Placing the current spike**
>
> Per UK guidance (IEE Wiring Matters), reliable results may be expected if the current spike is at least ten times the maximum dimension of the electrode system away from the electrode under test, for example 30 m for a 3 m rod.<sup>[R9 p.4](#sources-cited-on-this-page)</sup>

### Values to compare the result with

| Purpose | Value as published | Source |
|---|---|---|
| TT installation with a 30 mA RCD (UK) | RA × IΔn ≤ 50 V, approximately 1666 Ω<sup>[R9 p.5](#sources-cited-on-this-page)</sup><sup>[R9 p.5](#sources-cited-on-this-page)</sup> | IEE Wiring Matters |
| Measured loop impedance (UK) | above 200 Ω requires further investigation<sup>[R9 p.5](#sources-cited-on-this-page)</sup> | IEE GN3 via Wiring Matters |
| Building grounding electrode system (US DoD) | not over 25 Ω (5 Ω option), dry weather, not earlier than 48 hours after rain<sup>[R17 p.33](#sources-cited-on-this-page)</sup> | UFGS 27 05 26 |
| Lightning protection earth-termination | 10 Ω overall<sup>[R12 p.1](#sources-cited-on-this-page)</sup>; 10 Ω or less at low frequency, generally recommended<sup>[R6 p.128](#sources-cited-on-this-page)</sup> | Furse (UK); DEHN |
| High-site earthing (South Africa) | preferably below 10 Ω<sup>[R13 p.22](#sources-cited-on-this-page)</sup> | WAPA |

*Each value applies to the purpose and jurisdiction in its row. The earthing and bonding fundamentals sheet lists the full set of resistance values found in the sources.*

## 6  Surge protective devices: status and end of life

- BEAMA SPD guide (UK, 2018): periodic inspection first checks that the SPD's OCPD has not operated and that the SPD's fault indicator shows it serviceable.<sup>[R48 p.56](#sources-cited-on-this-page)</sup>
- ABB OVR brochure: the SPD's mechanical end-of-life indicator changes from white to red at end of life, after which the SPD must be changed as protection is no longer guaranteed.<sup>[R52 p.8](#sources-cited-on-this-page)</sup>
- ABB OVR brochure: a faulty SPD wired for continuity of service simply disconnects itself without interrupting the supply, but the equipment is then no longer protected.<sup>[R52 p.8](#sources-cited-on-this-page)</sup>
- ABB solar brochure (Lightning and surge protective devices, 2011): every SPD using MOVs must have an internal thermal disconnection so that it can be disconnected at end of life.<sup>[R51 p.3](#sources-cited-on-this-page)</sup>
- Per NIST (US), when the protective element of a surge protector fails, the internal disconnect works in one of two ways depending on the design: some protectors cut off the output power completely, others disconnect the failed element but keep the output powered.<sup>[R1 p.9](#sources-cited-on-this-page)</sup>
- Per NIST (US), specialists consider that most of the (rare) catastrophic failures of surge protectors are caused by excessively high line voltage occurring during a power-system fault, rather than by very large surges.<sup>[R1 p.18](#sources-cited-on-this-page)</sup>
- Per the South African WAPA high-site guideline, immediately after lightning damage, all earthing points, earth straps and surge protection devices should be inspected and repaired.<sup>[R13 p.30](#sources-cited-on-this-page)</sup>

### Insulation resistance tests with SPDs installed

- BEAMA SPD guide (UK, 2018): SPDs should be isolated during insulation resistance testing because they may operate on the test voltage.<sup>[R48 p.56](#sources-cited-on-this-page)</sup>
- BEAMA SPD guide (UK, 2018): during periodic testing, with the SPD's OCPD open a 500 V insulation resistance test is applied between live conductors and earth, expecting more than 1 megohm (BS 7671 Table 61).<sup>[R48 p.56](#sources-cited-on-this-page)</sup>
- BEAMA SPD guide (UK, BS 7671:2018 612.3.2): where an SPD cannot practically be disconnected (e.g. a fixed surge-protected socket outlet), insulation resistance is tested at 250 V between live conductors and earth.<sup>[R48 p.56](#sources-cited-on-this-page)</sup>
- BRE PV guide (UK, 2nd ed. 2006): before an array insulation resistance test, any equipment that could affect the measurement, i.e. overvoltage protection (SPDs) in the junction or combiner boxes, must be disconnected.<sup>[R49 p.28](#sources-cited-on-this-page)</sup>
- BEAMA SPD guide (UK, 2018): provision should be made for readily disconnecting the neutral conductors for testing, by 2-pole or 4-pole means of isolation.<sup>[R48 p.53](#sources-cited-on-this-page)</sup>

### Visual inspection of the surge protection system

- BEAMA SPD guide (UK, 2018): visual inspection of a surge protection system should verify that bonding conductors and cable shields are intact and cable segregation is maintained.<sup>[R48 p.57](#sources-cited-on-this-page)</sup>
- BEAMA SPD guide (UK, 2018): inspection should catch later additions such as a power line to external CCTV cameras or car-park lighting that crosses a lightning protection zone and needs an SPD.<sup>[R48 p.57](#sources-cited-on-this-page)</sup>
- BEAMA SPD guide (UK, BS 7671:2018): where SPDs are installed, a durable notice complying with BS 7671 should be fixed adjacent to the distribution board(s).<sup>[R48 p.55](#sources-cited-on-this-page)</sup>

> [!NOTE]
> **NOTE: Not covered by the sources in this library**
>
> No verified fact in this library describes remote signalling contacts on SPDs. Follow the SPD manufacturer's instructions for replacement.

## 7  RCD, PV and other commissioning tests

### RCDs and earth leakage

- Sunsynk 8 kW hybrid inverter manual: before switching on, the installation engineer must have completed the earth bond, RCD and earth leakage tests, checked that the PV Voc does not exceed 480 V and checked the battery voltage.<sup>[R46 p.68](#sources-cited-on-this-page)</sup>

### PV arrays and inverters

- SAPVIA PV guidelines (South Africa, 2017): according to IEC 62446, for each string the measurement of Voc and Isc and a polarity and isolation (insulation) check are mandatory, and as a minimum Voc and polarity must be checked before the strings are connected to the inverter.<sup>[R47 p.34](#sources-cited-on-this-page)</sup>
- BRE PV guide (UK, 2nd ed. 2006): one permitted array insulation test method is a test between array negative and earth followed by a test between array positive and earth (the other is between earth and the short-circuited array positive and negative).<sup>[R49 p.28](#sources-cited-on-this-page)</sup>
- BRE PV guide (UK, 2nd ed. 2006): for an array insulation test with positive and negative shorted together on a 120 V system, the test voltage is 250 V and the minimum insulation resistance is 0.25 megohm.<sup>[R49 p.29](#sources-cited-on-this-page)</sup>
- BRE PV guide (UK, 2nd ed. 2006): for separate insulation tests to array positive and array negative on systems below 600 V, the test voltage is 500 V minus Voc(stc) and the minimum insulation resistance is 0.5 megohm.<sup>[R49 p.29](#sources-cited-on-this-page)</sup>
- Sunsynk 8 kW hybrid inverter manual: before connecting to the grid the inverter measures the impedance of PV+ to ground and PV- to ground, and if either is below 33 kOhm it will not connect and reports error F24.<sup>[R46 p.69](#sources-cited-on-this-page)</sup>
- Sunsynk 8 kW hybrid inverter manual: fault F24 (DC insulation impedance failure, PV isolation resistance too low) calls for checking that the earth bond cable on the inverter is connected to ground.<sup>[R46 p.66](#sources-cited-on-this-page)</sup>
- SAPVIA PV guidelines (South Africa, 2017): the inverter automatically performs insulation checks for ground faults and issues a warning message when insulation resistance is insufficient, which should be addressed as soon as possible.<sup>[R47 p.36](#sources-cited-on-this-page)</sup>
- DEHN rooftop-PV white paper (WPX029, 2022): the insulation monitoring integrated in inverters is only permanently effective if the PV mounting system is connected to earth.<sup>[R44 p.2](#sources-cited-on-this-page)</sup>
- BRE PV guide (UK, 2nd ed. 2006): the installation check list covers, under protection against overvoltage/electric shock: array frame equipotential bonding present, surge protection devices present, RCD provided (each only if required), and frame correctly integrated with the existing LPS installation.<sup>[R49 p.27](#sources-cited-on-this-page)</sup>

### Electric fences

- Nemtek (Druid LCD 2x installer manual): after installation the fence must always be tested for correct short-circuit and open-circuit alarming at various points along the fence.<sup>[R30 p.12](#sources-cited-on-this-page)</sup>

## 8  Where the sources disagree

The sources were written for different countries and kinds of site. Where they conflict, the wiring code that applies at the site decides; this table shows the conflict rather than choosing for you.

| Question | One source says | Other sources say |
|---|---|---|
| How often to inspect the earthing | IEC 62305-3 via DEHN: by class of LPS, visual every 1 or 2 years, complete every 2 or 4 years.<sup>[R6 p.57](#sources-cited-on-this-page)</sup> | WAPA (South Africa, high sites): check the earthing system and inspect all earthing points once a year.<sup>[R13 p.30](#sources-cited-on-this-page)</sup><sup>[R13 p.30](#sources-cited-on-this-page)</sup> |
| Acceptable bonding resistance | DEHN: below 1 Ω for bonding and LPS connections.<sup>[R6 p.180](#sources-cited-on-this-page)</sup><sup>[R6 p.58](#sources-cited-on-this-page)</sup> | UFGS 27 05 26 (US DoD): 100 mΩ maximum, 50 mΩ for critical facilities<sup>[R17 p.33](#sources-cited-on-this-page)</sup>; cable-tray bonds at most 1 mΩ.<sup>[R17 p.18](#sources-cited-on-this-page)</sup> |
| Acceptable earth electrode resistance | UFGS 27 05 26 (US DoD): 25 Ω, or 5 Ω as an option.<sup>[R17 p.33](#sources-cited-on-this-page)</sup> | DEHN: 10 Ω or less for an LPS<sup>[R6 p.128](#sources-cited-on-this-page)</sup>; IEE Wiring Matters (UK): about 1666 Ω meets the 50 V rule with a 30 mA RCD, values above 200 Ω need investigation.<sup>[R9 p.5](#sources-cited-on-this-page)</sup><sup>[R9 p.5](#sources-cited-on-this-page)</sup> |

## 9  Printable inspection checklist

- [ ] Inspection of the lightning protection system done by a lightning protection specialist.<sup>[R6 p.56](#sources-cited-on-this-page)</sup>
- [ ] Earthing work carried out and certified by a competent registered person (South African practice per WAPA).<sup>[R13 p.20](#sources-cited-on-this-page)</sup>
- [ ] LPS inspected within the maximum interval for its class: visual and complete inspection dates recorded.<sup>[R6 p.57](#sources-cited-on-this-page)</sup>
- [ ] LPS inspected after any known strike and after changes, extensions or repairs to the structure.<sup>[R6 p.57](#sources-cited-on-this-page)</sup>
- [ ] All earthing points and earth straps inspected for damage, arcing or corrosion and repaired.<sup>[R13 p.30](#sources-cited-on-this-page)</sup>
- [ ] Continuity of air-terminations, down conductors, bonding conductors and shielding measured below 1 Ω.<sup>[R6 p.58](#sources-cited-on-this-page)</sup>
- [ ] Bonding continuity tested with a 200 mA test current (IEC 60364-6, IEC 61557-4).<sup>[R6 p.180](#sources-cited-on-this-page)</sup>
- [ ] Installation isolated at the main switch-disconnector before the earth electrode test.<sup>[R9 p.5](#sources-cited-on-this-page)</sup>
- [ ] Earth electrode resistance measured, ideally in the least favourable (dry) ground conditions, with the current spike at least ten times the maximum dimension of the electrode system away.<sup>[R9 p.4](#sources-cited-on-this-page)</sup><sup>[R9 p.4](#sources-cited-on-this-page)</sup>
- [ ] Means of earthing re-established before the installation is energised.<sup>[R9 p.5](#sources-cited-on-this-page)</sup>
- [ ] Earth leakage protection devices tested (WAPA: once a year).<sup>[R13 p.30](#sources-cited-on-this-page)</sup>
- [ ] SPDs inspected and repaired after lightning damage.<sup>[R13 p.30](#sources-cited-on-this-page)</sup>
- [ ] Each SPD's overcurrent protective device not operated and its fault indicator showing it serviceable.<sup>[R48 p.56](#sources-cited-on-this-page)</sup>
- [ ] SPDs isolated during insulation resistance testing.<sup>[R48 p.56](#sources-cited-on-this-page)</sup>
- [ ] Bonding conductors and cable shields intact and cable segregation maintained.<sup>[R48 p.57](#sources-cited-on-this-page)</sup>
- [ ] Later additions (for example a power line to outdoor cameras) that cross a lightning protection zone checked for an SPD.<sup>[R48 p.57](#sources-cited-on-this-page)</sup>
- [ ] Durable SPD notice fixed next to the distribution board (UK, BS 7671:2018).<sup>[R48 p.55](#sources-cited-on-this-page)</sup>
- [ ] PV array SPDs disconnected before an array insulation resistance test.<sup>[R49 p.28](#sources-cited-on-this-page)</sup>
- [ ] Before switching on a PV inverter: earth bond, RCD and earth leakage tests completed.<sup>[R46 p.68](#sources-cited-on-this-page)</sup>
- [ ] Voltage tested for on PV parts before touching them.<sup>[R49 p.21](#sources-cited-on-this-page)</sup>

## Sources cited on this page

`[R18 p.12]` = reference 18 below, PDF page 12 (page index of the PDF file). Each cited statement was checked against a verbatim quote from that page.

| Ref | Document | PDF pages cited |
|---|---|---|
| R1 | **Surges Happen! How to Protect the Appliances in Your Home (NIST Special Publication 960-6)** — National Institute of Standards and Technology (USA) · May 2001 · USA · [link](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication960-6.pdf) | 9-10, 18 |
| R6 | **Lightning Protection Guide, 3rd updated edition** — DEHN + SÖHNE · 2014 · IEC / EN 62305 (Germany) · [link](https://www.dehn-international.com/sites/default/files/media/files/lpg_en_complete.pdf) | 56-58, 128, 131, 180, 220 |
| R9 | **Multiple earth electrodes in a TT system for a dwelling (IET Wiring Matters, Winter 2006)** — The Institution of Engineering and Technology (UK) · Winter 2006 · UK (BS 7671) · [link](https://electrical.theiet.org/media/1659/multiple-earth-electrodes-in-a-tt-system-for-a-dwelling.pdf) | 3-5 |
| R12 | **IEC/BS EN 62305 parts 1-4: technical reference (Furse)** — ABB Furse · not stated in document · IEC / BS EN 62305 (UK) · [link](https://library.e.abb.com/public/ee4d371685e544e09e8d9712fbd716c9/IEC%20BS%20EN%2062305%201%20-%204.pdf) | 1 |
| R13 | **Wireless High Site Engineering Guideline V1.0.0** — Wireless Access Providers' Association (South Africa) · V1.0.0, 2014-07-21 · South Africa · [link](https://wapa.org.za/sites/default/files/2018-08/WAPA%20Wireless%20High%20Site%20Engineering%20Guideline%20V1%200%200%2020140721.pdf) | 20-22, 30 |
| R17 | **UFGS-27 05 26 Grounding and Bonding for Communications Systems** — USACE / NAVFAC / AFCEC (US Department of Defense) · November 2025 · USA (guide specification with designer-selectable options) · [link](https://www.wbdg.org/FFC/DOD/UFGS/UFGS%2027%2005%2026.pdf) | 10, 18, 33-34 |
| R21 | **Grounding (RouterOS documentation, hardware section)** — MikroTik · page last updated 23 September 2025 · International · [link](https://help.mikrotik.com/docs/display/ROS/Grounding) | 1 |
| R23 | **Recommendation ITU-T K.73: Shielding and bonding for cables between buildings** — International Telecommunication Union · 11/2019 · International · [link](https://www.itu.int/rec/T-REC-K.73-201911-I) | 9 |
| R24 | **Recommendation ITU-T K.27: Bonding configurations and earthing inside a telecommunication building** — International Telecommunication Union · 03/2015 · International · [link](https://www.itu.int/rec/T-REC-K.27-201503-I) | 18 |
| R28 | **LOGO! System Manual, A5E33039675-AL** — Siemens AG · 03/2023 · International · [link](https://cache.industry.siemens.com/dl/files/499/109826499/att_1161914/v1/logo_system_manual_en-US_en-US.pdf) | 31 |
| R30 | **DRUID LCD 2x Electric Fence Energizer: Installer Manual, Revision 1.2** — Nemtek Group · 25 September 2013 · South Africa · [link](https://nemtek.co.za/wp-content/uploads/2021/11/installer-manual-druid-2.pdf) | 12 |
| R32 | **Super Earthing Kit EA-CEC/KIT: Instruction Manual** — Nemtek Group · file dated November 2025 · South Africa · [link](https://www.nemtek.co.za/wp-content/uploads/2025/03/SuperEarthingKit111125.pdf) | 2 |
| R33 | **D5-Evo light-industrial sliding gate operator: installation manual** — Centurion Systems (Pty) Ltd · not stated on the pages read · South Africa · [link](https://cdn.shopify.com/s/files/1/0398/4615/0189/files/D5-Evo_Installation_Manual.pdf) | 31 |
| R44 | **White paper WPX029: Lightning and surge protection for rooftop photovoltaic systems** — DEHN SE · WPX029/EN/0422 (April 2022) · IEC / EN (Germany) · [link](https://www.dehn-africa.com/sites/default/files/media/files/photovoltaic-wpx029-en.pdf) | 2 |
| R45 | **Technical Information: Overvoltage Protection. Lightning Protection and Overvoltage Protection for Sunny Boy and Sunny Tripower (U_Schutz-TI-en-13)** — SMA Solar Technology AG · version 1.3 · International · [link](https://files.sma.de/downloads/U_Schutz-TI-en-13.pdf) | 1 |
| R46 | **Hybrid Parity (Super) Inverter User Manual, SUNSYNK-8K-SG01LP1 / SUNSYNK-8K-SG03LP1** — Sunsynk (Global Tech China Ltd) · v.18 (12/09/22) · International · [link](https://cdn.shopify.com/s/files/1/0521/6006/9799/files/sunsynk_8kw_manual.pdf) | 6, 66, 68-69 |
| R47 | **Solar PV Installation Guidelines, Iteration 1.0 (PV GreenCard)** — South African Photovoltaic Industry Association (SAPVIA) · May 2017 · South Africa · [link](https://portal.segensolar.co.za/reseller/docs/SAPVIASolarPVGuidelines.pdf) | 28, 34, 36 |
| R48 | **BEAMA Guide to Surge Protection Devices (SPDs): selection, application and theory** — BEAMA Ltd (UK) · July 2018 · UK (BS 7671:2018) · [link](https://www.beama.org.uk/static/uploaded/0125b82e-8c76-4106-88bedb0f4fc85d52.pdf) | 53, 55-57 |
| R49 | **Photovoltaics in Buildings: Guide to the installation of PV systems, 2nd edition (DTI/Pub URN 06/1972)** — UK Department for Enterprise (DTI) / BRE · 2006 · UK · [link](https://files.bregroup.com/solar/Guide_to_the_installation_of_PV_systems_2nd_Edition.pdf) | 5, 21-22, 27-29 |
| R51 | **Solar energy: lightning and surge protective devices (brochure 1TXH 000 118 B0201)** — ABB · 2011 · IEC · [link](https://library.e.abb.com/public/77266805bb3868adc12578f10033b12b/1TXH%20000%20118%20B0201_Solar%20energy%20Lightning%20and%20overvoltage%20protection_br.pdf) | 3 |
| R52 | **System pro M compact: OVR surge protective devices (main catalogue 1TXH000083C0201)** — ABB · 2011 · IEC · [link](https://library.e.abb.com/public/d614bdefa272767ac125784c005b65e8/1TXH000083C0201_ABB%20OVR%20%20RANGE%20SYSTEM%20proM_2011.pdf) | 8 |

*Generated from `content/docs/12_inspection_testing.yaml` on 2026-11-24. Do not edit this page in the wiki; edit the content file.*
