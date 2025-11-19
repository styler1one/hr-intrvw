# 🎯 HR Interview Agent - Verbeterplan

**Datum**: 19 november 2025  
**Applicatie**: http://hr.agentboss.nl  
**Status**: Prioriteiten gesorteerd op impact

---

## 🔴 KRITIEKE VERBETERINGEN (Impact: 9-10/10)

### ⬜ 1. Voortgangsbalk blijft op 0-1%
**Impact**: 10/10 | **Tijd**: 2 uur  
**Probleem**: Na 3 vragen staat de voortgang nog op 1%, dit geeft gebruikers het gevoel dat het interview eindeloos duurt  
**Oplossing**: Dynamische voortgang per vraag binnen fase, niet alleen per fase  
**Code locatie**: `updateProgress()` functie in `public/index.html`  
**Verwachte verbetering**: Gebruikers voelen progressie en blijven gemotiveerd

### ⬜ 2. Geen visuele feedback tijdens AI response
**Impact**: 9/10 | **Tijd**: 1 uur  
**Probleem**: Na Enter drukken gebeurt er niets zichtbaars totdat de AI antwoordt (kan 2-5 seconden duren)  
**Oplossing**: Typing indicator direct tonen bij versturen  
**Code locatie**: `sendMessage()` functie  
**Verwachte verbetering**: Gebruiker weet dat systeem werkt, minder frustratie

### ⬜ 3. PDF bestandsnaam is onleesbaar
**Impact**: 9/10 | **Tijd**: 30 min  
**Probleem**: `Volentis_Interview_Wij_zijn_een_IT_bedrijf_met_250_medewerkers__actie____2025-11-19.pdf`  
**Oplossing**: `Volentis_Interview_[Organisatienaam]_2025-11-19.pdf` of laat gebruiker naam kiezen  
**Code locatie**: `exportSessionPDF()` functie  
**Verwachte verbetering**: Professioneler, makkelijker terug te vinden

---

## 🟠 HOGE PRIORITEIT (Impact: 7-8/10)

### ⬜ 4. Geen keyboard shortcuts
**Impact**: 8/10 | **Tijd**: 3 uur  
**Probleem**: Power users kunnen niet snel navigeren  
**Oplossing**: 
- `ESC` = sluit modals
- `Tab` = navigeer door suggesties
- `Ctrl/Cmd + K` = zoek sessies
- `Ctrl/Cmd + N` = nieuw interview  
**Verwachte verbetering**: 30% snellere workflow voor terugkerende gebruikers

### ⬜ 5. AI Suggesties verdwijnen bij typen
**Impact**: 8/10 | **Tijd**: 1 uur  
**Probleem**: Zodra je begint te typen, verdwijnen de suggesties - je kunt ze niet meer zien als inspiratie  
**Oplossing**: Houd suggesties zichtbaar, maar dim ze of verplaats ze naar boven  
**Verwachte verbetering**: Gebruikers kunnen suggesties als referentie gebruiken

### ⬜ 6. Geen auto-save indicator
**Impact**: 7/10 | **Tijd**: 1 uur  
**Probleem**: Gebruiker weet niet of antwoorden automatisch worden opgeslagen  
**Oplossing**: Kleine "Opgeslagen" indicator na elk antwoord (zoals Google Docs)  
**Code locatie**: Na `saveSessions()` call  
**Verwachte verbetering**: Vertrouwen dat data niet verloren gaat

### ⬜ 7. Sidebar te smal voor lange titels
**Impact**: 7/10 | **Tijd**: 1 uur  
**Probleem**: "Wij zijn een IT-bedrijf me..." wordt afgekort, niet duidelijk welke sessie het is  
**Oplossing**: Tooltip on hover met volledige titel, of bredere sidebar  
**Code locatie**: `renderSessions()` functie  
**Verwachte verbetering**: Betere sessie-identificatie

---

## 🟡 MEDIUM PRIORITEIT (Impact: 5-6/10)

### ⬜ 8. Geen undo functie voor verzonden berichten
**Impact**: 6/10 | **Tijd**: 2 uur  
**Probleem**: Als je per ongeluk Enter drukt, kun je bericht niet meer terugtrekken  
**Oplossing**: "Undo" knop voor laatste bericht (5 seconden window)  
**Verwachte verbetering**: Minder frustratie bij tikfouten

### ⬜ 9. Template selector heeft geen "Aanbevolen" badge
**Impact**: 6/10 | **Tijd**: 15 min  
**Probleem**: Nieuwe gebruikers weten niet welke template ze moeten kiezen  
**Oplossing**: "Meest gekozen" of "Aanbevolen" badge op Standard Interview  
**Code locatie**: `showTemplateSelector()` functie  
**Verwachte verbetering**: Snellere beslissing, minder twijfel

### ⬜ 10. Geen export naar andere formaten
**Impact**: 6/10 | **Tijd**: 4 uur  
**Probleem**: Alleen PDF export, geen Word/Excel/JSON  
**Oplossing**: Export opties: PDF, DOCX, JSON (voor integraties)  
**Verwachte verbetering**: Flexibiliteit voor verschillende use cases

### ⬜ 11. Geen sessie tags/labels
**Impact**: 5/10 | **Tijd**: 3 uur  
**Probleem**: Bij veel sessies is het lastig om ze te organiseren  
**Oplossing**: Tags toevoegen (bijv. "Q4 2024", "IT Sector", "Urgent")  
**Verwachte verbetering**: Betere organisatie bij power users

### ⬜ 12. Geen bulk acties in sidebar
**Impact**: 5/10 | **Tijd**: 2 uur  
**Probleem**: Kan niet meerdere sessies tegelijk verwijderen/exporteren  
**Oplossing**: Checkbox selectie + bulk acties  
**Verwachte verbetering**: Efficiënter sessie management

---

## 🟢 LAGE PRIORITEIT (Impact: 3-4/10)

### ⬜ 13. Geen animaties bij fase overgang
**Impact**: 4/10 | **Tijd**: 2 uur  
**Probleem**: Fase overgang is abrupt, geen visuele celebratie  
**Oplossing**: Confetti/checkmark animatie bij fase completion  
**Verwachte verbetering**: Meer engagement, gamification

### ⬜ 14. Dark mode contrast kan beter
**Impact**: 4/10 | **Tijd**: 1 uur  
**Probleem**: Sommige teksten zijn moeilijk leesbaar in dark mode  
**Oplossing**: WCAG AAA contrast ratio voor alle teksten  
**Verwachte verbetering**: Betere accessibility

### ⬜ 15. Geen email reminder voor gepauzeerde interviews
**Impact**: 4/10 | **Tijd**: 4 uur  
**Probleem**: Gebruikers vergeten gepauzeerde interviews af te maken  
**Oplossing**: Optionele email reminder na 24 uur  
**Verwachte verbetering**: Hogere completion rate

### ⬜ 16. Geen interview preview
**Impact**: 3/10 | **Tijd**: 2 uur  
**Probleem**: Kan niet zien wat er in een sessie staat zonder te openen  
**Oplossing**: Hover preview met eerste 3 Q&A's  
**Verwachte verbetering**: Sneller de juiste sessie vinden

---

## 🎨 UI/DESIGN VERBETERINGEN

### ⬜ 17. Inconsistente spacing
**Impact**: 5/10 | **Tijd**: 2 uur  
**Probleem**: Sommige elementen hebben te veel/weinig ruimte  
**Oplossing**: Consistent 8px grid systeem toepassen  
**Verwachte verbetering**: Professioneler uiterlijk

### ⬜ 18. AI Suggesties kunnen visueel beter
**Impact**: 5/10 | **Tijd**: 1 uur  
**Probleem**: Suggesties lijken te veel op gewone buttons  
**Oplossing**: Subtielere styling, gradient border, sparkle icon  
**Code locatie**: `showSuggestions()` functie CSS  
**Verwachte verbetering**: Duidelijker dat het AI-gegenereerd is

### ⬜ 19. Geen empty state illustraties
**Impact**: 4/10 | **Tijd**: 1 uur  
**Probleem**: Lege sidebar ziet er kaal uit  
**Oplossing**: Friendly illustratie + call-to-action  
**Verwachte verbetering**: Warmer, uitnodigender gevoel

---

## 🏗️ ARCHITECTUUR VERBETERINGEN

### ⬜ 20. Geen offline support
**Impact**: 6/10 | **Tijd**: 6 uur  
**Probleem**: Als internet wegvalt, verlies je alles  
**Oplossing**: Service Worker + IndexedDB voor offline draft saving  
**Verwachte verbetering**: Betrouwbaarheid, geen data verlies

### ⬜ 21. Geen real-time collaboration
**Impact**: 5/10 | **Tijd**: 8 uur  
**Probleem**: Kan niet samen met collega interview doen  
**Oplossing**: WebSocket voor real-time co-editing  
**Verwachte verbetering**: Team collaboration mogelijk

### ⬜ 22. Geen analytics/insights
**Impact**: 7/10 | **Tijd**: 3 uur  
**Probleem**: Geen inzicht in waar gebruikers afhaken of vastlopen  
**Oplossing**: Privacy-friendly analytics (Plausible/Fathom)  
**Verwachte verbetering**: Data-driven improvements

---

## 📱 MOBILE RESPONSIVENESS

### ✅ 23. Sidebar overlay op mobile
**Impact**: 8/10 | **Tijd**: 3 uur | **Voltooid**: 19 nov 2025  
**Probleem**: Sidebar neemt te veel ruimte op mobile  
**Oplossing**: Hamburger menu op mobile, slide-in sidebar  
**Verwachte verbetering**: Betere mobile UX  
**Implementatie**:
- Mobile header met hamburger menu (alleen zichtbaar op <768px)
- Sidebar slide-in van links met smooth transition
- Dark backdrop overlay bij open sidebar
- Auto-close bij sessie selectie
- Body scroll prevention bij open sidebar

### ⬜ 24. Touch targets te klein
**Impact**: 7/10 | **Tijd**: 2 uur  
**Probleem**: Suggestie buttons zijn moeilijk te tappen op mobile  
**Oplossing**: Minimum 44x44px touch targets  
**Verwachte verbetering**: Minder mis-taps

---

## 🎯 TOP 5 QUICK WINS

Prioriteer deze voor maximale impact met minimale tijd:

1. ⬜ **Voortgangsbalk fix** (10/10) - 2 uur werk
2. ⬜ **PDF bestandsnaam** (9/10) - 30 min werk  
3. ⬜ **Typing indicator bij verzenden** (9/10) - 1 uur werk
4. ⬜ **Auto-save indicator** (7/10) - 1 uur werk
5. ⬜ **Template "Aanbevolen" badge** (6/10) - 15 min werk

**Totale impact**: 41/50 punten in ~5 uur werk 🚀

---

## ✅ WAT ER AL GOED IS

- ✅ Clean, moderne UI
- ✅ AI suggesties werken goed
- ✅ Toast notifications zijn duidelijk
- ✅ Dark mode implementatie
- ✅ PDF export functionaliteit
- ✅ Pauzeren/hervatten werkt goed
- ✅ Sessie management is intuïtief
- ✅ Responsive design basis is goed

---

## 📊 VOORTGANG TRACKING

**Totaal taken**: 24  
**Voltooid**: 1 ✅  
**In progress**: 0  
**Te doen**: 23  

**Geschatte totale tijd**: ~60 uur  
**Quick wins tijd**: ~5 uur  
**Bestede tijd**: 3 uur

---

## 📝 NOTITIES

- Gebruik `⬜` voor open taken, `✅` voor voltooide taken
- Update deze file na elke voltooide taak
- Prioriteer op basis van impact én beschikbare tijd
- Test elke verbetering grondig voor deployment

---

**Laatste update**: 19 november 2025
