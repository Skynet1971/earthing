> Earthing, Bonding, Surge & Lightning Protection Library · **VISUAL GUIDE 1 · EARTHING** · content version 1.0

# Visual guide 1: how earthing and bonding work

*Animated pictures of the fault path, the supply earthing systems and why every earth must meet at one point*

**Applies to:** Anyone who wants to see how the earth connection of a house works before reading the reference sheets

📄 **PDF:** [14_visual_guide_earthing_bonding.pdf](https://github.com/Skynet1971/earthing/raw/HEAD/docs/pdf/14_visual_guide_earthing_bonding.pdf)

> ℹ️ Information only. Every technical statement cites a source and PDF page; it does not replace the wiring code that applies at the site, the product manuals, or a qualified and registered person.

## 1  The earth path makes a fault switch itself off

In a TN-C-S supply the PEN conductor provides the household earth and carries the earth-fault current back to the distribution transformer.<sup>[R64 p.4](#sources-cited-on-this-page)</sup>

<a href="img/ex_fault_path.svg"><img src="img/ex_fault_path.svg" alt="ex_fault_path" width="100%"></a>

*Animated: the steps play in a loop. Click to open full size.* (1) In normal use the current returns on the neutral. (2) When a live conductor touches an earthed metal case, the fault current returns on the protective earth and the PEN to the transformer.<sup>[R64 p.4](#sources-cited-on-this-page)</sup> TN-C-S is used so that this fault current does not depend on soil resistivity.<sup>[R64 p.4](#sources-cited-on-this-page)</sup> (3) In TN systems, fault touch voltages in circuits with socket outlets must be disconnected automatically within 0.4 s.<sup>[R6 p.220](#sources-cited-on-this-page)</sup>

| **0.4 s** | **0.35 Ω** | **0.8 Ω** |
|---|---|---|
| maximum disconnection time, socket-outlet circuits, TN systems<sup>[R6 p.220](#sources-cited-on-this-page)</sup> | maximum Ze for TN-C-S (PME) supplies, UK distributor figure<sup>[R8 p.5](#sources-cited-on-this-page)</sup> | maximum Ze for TN-S supplies, UK distributor figure<sup>[R8 p.5](#sources-cited-on-this-page)</sup> |

## 2  Supply earthing systems at a glance

<a href="img/earthing_systems.svg"><img src="img/earthing_systems.svg" alt="earthing_systems" width="100%"></a>

*Click the diagram to open it full size.* *Concept sketch. (2) TN-C-S: the PEN conductor of the supply provides the household earth, as Louw and Bokoro describe for South African networks.<sup>[R64 p.4](#sources-cited-on-this-page)</sup> (3) TT: the consumer must provide their own connection to earth with a local earth electrode (UK guidance)<sup>[R8 p.8](#sources-cited-on-this-page)</sup>; the electrode resistance multiplied by the rated residual operating current of the protective device must not exceed 50 V (UK, BS 7671:2001).<sup>[R9 p.5](#sources-cited-on-this-page)</sup>*

- BS 7671 (UK) lists five types of earthing system: TN-S, TN-C-S, TT, TN-C and IT.<sup>[R8 p.2](#sources-cited-on-this-page)</sup>
- Louw and Bokoro (SAIEE Africa Research Journal, Dec 2019): LV earthing in South African networks follows IEC 60364 and SANS 10292, using TN-C and TN-C-S configurations; the PEN conductor provides the household earth and lets earth-fault (zero-sequence) current return to the distribution transformer star point, avoiding dependence on soil resistivity for the fault current needed to operate protection.<sup>[R64 p.4](#sources-cited-on-this-page)</sup>
- ECA(SA) (2024) quoting SANS 10142-1 7.12.3.1.1 Note 1: in a TN system earthing of the electricity supply, an earth electrode is normally not required in an electrical installation.<sup>[R69 p.4](#sources-cited-on-this-page)</sup>
- BS 7671:2001 Regulation 413-02-20 (UK) states that for TT systems the earth electrode resistance RA multiplied by the operating current of the protective device (rated residual operating current) must not exceed 50 V.<sup>[R9 p.5](#sources-cited-on-this-page)</sup>
- Per UK guidance (IEE Wiring Matters), for an RCD rated at 30 mA the 50 V rule equates to an earth electrode resistance limit of approximately 1666 Ω.<sup>[R9 p.5](#sources-cited-on-this-page)</sup>

## 3  Every earth meets at one point

For electronic equipment the sources ask for one bonding point, short conductors, and no separate earth that is not bonded to it.<sup>[R18 p.18](#sources-cited-on-this-page)</sup><sup>[R6 p.142](#sources-cited-on-this-page)</sup><sup>[R18 p.19](#sources-cited-on-this-page)</sup>

<a href="img/common_bonding.svg"><img src="img/common_bonding.svg" alt="common_bonding" width="100%"></a>

*Click the diagram to open it full size.* *Concept sketch, not a wiring diagram. (1) all services connected with low-impedance bonding conductors to the main earth terminal, low impedance being obtained by keeping them shorter than 1.5 m (ITU-T K.66)<sup>[R18 p.19](#sources-cited-on-this-page)</sup> (2) earthing connects the earth bar to earth, usually via an installed electrode (ITU-T K.98)<sup>[R25 p.27](#sources-cited-on-this-page)</sup> (3) every earth point bonded to the main earth bar, with nothing connected to a separate electrode that is not bonded to it (ITU-T K.66).<sup>[R18 p.18](#sources-cited-on-this-page)</sup>*

<a href="img/ex_potential_difference.svg"><img src="img/ex_potential_difference.svg" alt="ex_potential_difference" width="100%"></a>

*Animated: the steps play in a loop. Click to open full size.* ITU-T K.66 example: without a common bonding point, a 50 A surge from the telecom line through a 300 Ω earth electrode raises the telecom equipment 15 kV above the power network.<sup>[R18 p.58](#sources-cited-on-this-page)</sup> Of the customer earthing practices K.66 examined, only the common earth bar with short bond wires protects equipment from surges entering on external cables without additional protection.<sup>[R18 p.56](#sources-cited-on-this-page)</sup>

> [!CAUTION]
> **DO NOT: No separate 'clean earth'**
>
> DEHN calls a separate clean earth for electronic equipment, kept apart from the lightning protection and protective earth, extremely unfavourable and potentially dangerous.<sup>[R6 p.142](#sources-cited-on-this-page)</sup>

## 4  Earth electrodes

| **15 mm** | **2.5 m** | **90 %** |
|---|---|---|
| minimum diameter, solid round copper earth rod (IEC 62305-3 Table 7)<sup>[R6 p.149](#sources-cited-on-this-page)</sup> | one permitted antenna earth electrode: a vertical rod this long (IEC 60728-11)<sup>[R6 p.292](#sources-cited-on-this-page)</sup> | of the resistance lies within 5 m of a 20 cm sphere electrode (DEHN example)<sup>[R6 p.121](#sources-cited-on-this-page)</sup> |

- Per UK guidance (IET), earth rods should be driven into virgin ground, not disturbed (backfilled) ground.<sup>[R8 p.3](#sources-cited-on-this-page)</sup>
- Per UK guidance (IET, 2011), where two or more earth rods are driven and connected together, the separation between rods should be at least equal to their combined driven depth to obtain maximum advantage from each rod.<sup>[R8 p.3](#sources-cited-on-this-page)</sup>
- Per UK guidance (IEE Wiring Matters), with multiple earth rods in parallel the overall resistance is virtually proportional to the reciprocal of the number of rods, provided each rod is outside the resistance area (sphere of influence) of any other.<sup>[R9 p.3](#sources-cited-on-this-page)</sup>
- Per UK guidance (IET), whatever form an earth electrode takes, the possibility of soil drying and freezing, and of corrosion, must be taken into account.<sup>[R8 p.3](#sources-cited-on-this-page)</sup>
- InstMC Tech Talk 12 (UK, 2017): a soil resistivity test is the main factor in determining the type and extent of the earth electrode(s) required.<sup>[R43 p.3](#sources-cited-on-this-page)</sup>

## Sources cited on this page

`[R18 p.12]` = reference 18 below, PDF page 12 (page index of the PDF file). Each cited statement was checked against a verbatim quote from that page.

| Ref | Document | PDF pages cited |
|---|---|---|
| R6 | **Lightning Protection Guide, 3rd updated edition** — DEHN + SÖHNE · 2014 · IEC / EN 62305 (Germany) · [link](https://www.dehn-international.com/sites/default/files/media/files/lpg_en_complete.pdf) | 121, 142, 149, 220, 292 |
| R8 | **Earthing: your questions answered (IET Wiring Matters, Autumn 2011)** — The Institution of Engineering and Technology (UK) · Autumn 2011 · UK (BS 7671) · [link](https://electrical.theiet.org/media/1549/earthing.pdf) | 2-3, 5, 8 |
| R9 | **Multiple earth electrodes in a TT system for a dwelling (IET Wiring Matters, Winter 2006)** — The Institution of Engineering and Technology (UK) · Winter 2006 · UK (BS 7671) · [link](https://electrical.theiet.org/media/1659/multiple-earth-electrodes-in-a-tt-system-for-a-dwelling.pdf) | 3, 5 |
| R18 | **Recommendation ITU-T K.66: Protection of customer premises from overvoltages** — International Telecommunication Union · 11/2019 · International · [link](https://www.itu.int/rec/T-REC-K.66-201911-I) | 18-19, 56, 58 |
| R25 | **Recommendation ITU-T K.98: Overvoltage protection guide for telecommunication equipment installed in customer premises** — International Telecommunication Union · 08/2014 · International · [link](https://www.itu.int/rec/T-REC-K.98-201408-I) | 27 |
| R43 | **Tech Talk (12) Down to Earth: A Discussion of the General Requirements for the Earthing of Control and Instrumentation Systems** — Institute of Measurement and Control; Measurement and Control 2017, Vol. 50(2) 39-44 · 2017 · UK · [link](https://www.instmc.org/_userfiles/pages/files/technical/tech_talk_12_down_to_earth.pdf) | 3 |
| R64 | **An Alternative technique for the detection and mitigation of electricity theft in South Africa** — SAIEE Africa Research Journal (South African Institute of Electrical Engineers); authors Quentin Louw and Pitshou Bokoro · Vol.110 (4) December 2019 · South Africa · [link](https://scielo.org.za/pdf/arj/v110n4/03.pdf) | 4 |
| R69 | **Neutral Earth Bonding Clarified** — Electrical Contractors' Association (South Africa), ECA(SA); author Nicholas McDiarmid · 18 January 2024 · South Africa · [link](https://ecasa.co.za/technical/neutral-earth-bonding-clarified/) | 4 |

*Generated from `content/docs/14_visual_guide_earthing.yaml` on 2026-11-25. Do not edit this page in the wiki; edit the content file.*
