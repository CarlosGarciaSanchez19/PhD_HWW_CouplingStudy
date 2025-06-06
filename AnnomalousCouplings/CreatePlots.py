
from math import sqrt
import sys
import os
import ROOT

src  = os.path.realpath("rootFiles__2016HIPM_v9/mkShapes__2016HIPM_v9_ggHvsVBF_MoMEMta_jets_TFs.root")

normalise = True
plot = False

method = "MoMEMta"
Low = ""
cat  = "hww2l2v_13TeV_of2j_vbf" + Low
var  = "D_ggHvsHVBF"
folder = method + "/"
var_unity = ""
prod = "qqH_hww"
prod2 = "ggH_hww"
bkg = "WW"

########

f = ROOT.TFile.Open(''+src+'', 'read')
hstr = ''+cat+'/'+var+'/histo_'+prod
h1 = f.Get(""+hstr+"")
h2 = f.Get(hstr.replace('qqH_hww', prod2))
hstr = ''+cat+'/'+var+'/histo_'+bkg
hbkg = f.Get(""+hstr+"")
h1.SetDirectory(0)
h2.SetDirectory(0)
hbkg.SetDirectory(0)
f.Close()

print("Greater than 0.8 window qqH events for "+method+" (with jets TFs):", h1.Integral(8, 10))
print("Greater than 0.8 window WW events for "+method+" (with jets TFs):", hbkg.Integral(8, 10))
print("Significance for "+method+":", h1.Integral(8, 10) / sqrt(hbkg.Integral(8, 10)))

if plot:
    canvas = ROOT.TCanvas('canvas', '', 700, 500)
    ROOT.gStyle.SetOptStat(0)
    h1.SetLineColor(ROOT.kBlack)
    h1.SetLineWidth(2)
    h1.SetMarkerColor(ROOT.kBlack)
    h1.SetMarkerStyle(20)
    h1.SetMarkerSize(0.4)
    h1.SetFillColor(ROOT.kBlack)
    h1.SetFillStyle(0)
    h2.SetLineColor(ROOT.kRed)
    h2.SetLineWidth(2)
    h2.SetMarkerColor(ROOT.kRed)
    h2.SetMarkerStyle(20)
    h2.SetMarkerSize(0.4)
    h2.SetFillColor(ROOT.kRed)
    h2.SetFillStyle(0)

    if (Low == "L"):
        h1.SetTitle(r"D_{ggH vs HVBF}"+" including low-energy jets"+" ("+method+" output)")
    else:
        h1.SetTitle(r"D_{ggH vs HVBF}"+" ("+method+" output)")
    h1.GetXaxis().SetTitle(r"D_{ggH vs HVBF}"+" "+var_unity)
    #h1.GetYaxis().SetTitle('Events')
    if (normalise):
        h1.Scale(1/h1.Integral())
        h2.Scale(1/h2.Integral())
        hbkg.Scale(1/hbkg.Integral())
    # h1.Scale(1/h1.GetMaximum())
    #     h2.Scale(1/h2.GetMaximum())
    #     hbkg.Scale(1/hbkg.GetMaximum())
    else:
        h1.Scale(hbkg.Integral())
    hbkg.SetLineColor(ROOT.kBlue)
    hbkg.SetLineWidth(2)
    hbkg.SetMarkerColor(ROOT.kBlue)
    hbkg.SetFillColor(ROOT.kBlue)
    hbkg.SetFillStyle(0)
    hbkg.SetMarkerStyle(20)
    hbkg.SetMarkerSize(0.4)
    # h1.Draw("")
    # h2.Draw("same")
    # hbkg.Draw("same")
    h1.Draw("HIST")
    h2.Draw("same HIST")
    hbkg.Draw("same HIST")
    h1.GetYaxis().SetRangeUser(.0, .8) # only if needed
    h1.GetXaxis().SetRangeUser(0., 1.) # only if needed
    legend = ROOT.TLegend(0.65, 0.65, 0.85, 0.85)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.035)
    legend.SetFillStyle(0)
    legend.AddEntry(h1, 'qqH', "l")
    legend.AddEntry(h2, 'ggH', "l")
    legend.AddEntry(hbkg, bkg+"_bkg", "l")
    legend.Draw("same")
    canvas.SaveAs("plots/pdfs/"+folder+cat+"_"+var+"_"+prod+"_with_"+bkg+"bkg_"+method+"_with_jets_TFs.pdf")
    canvas.SaveAs("plots/pngs/"+folder+cat+"_"+var+"_"+prod+"_with_"+bkg+"bkg_"+method+"_with_jets_TFs.png")

