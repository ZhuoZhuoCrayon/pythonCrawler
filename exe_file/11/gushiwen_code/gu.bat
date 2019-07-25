cd C:\Users\crayon\OneDrive\Pycode\Crawler\crawler_Basic\exe_file\11\gushiwen_code

echo font 0 0 0 0 0>font_properties

echo Run Tesseract for Training..
tesseract.exe --psm 10 gu.font.exp0.tif gu.font.exp0 nobatch box.train



echo Compute the Character Set..
unicharset_extractor.exe gu.font.exp0.box


mftraining -F font_properties -U unicharset -O gu.unicharset gu.font.exp0.tr

echo Clustering..
cntraining.exe gu.font.exp0.tr

echo Rename Files..


rename normproto gu.normproto

rename inttemp gu.inttemp


rename pffmtable gu.pffmtable


rename shapetable gu.shapetable



echo Create Tessdata..


combine_tessdata.exe gu.
