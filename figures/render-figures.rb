#!/usr/bin/env ruby

require "rexml/document"
include REXML

def rebrand(fname, brand)
  svg = Document.new(File.new(fname, 'r'))
  temp = 
  svg.root.each_element("/svg/g/rect[@id='background']") do |e|
    e.attributes["style"] = "fill:url(##{brand});"
    puts e
  end
  temp_f = File.new(TEMP,'w+')
  temp_f.puts svg
  temp_f.close
  File.delete(TEMP)
end

TEMP = './tmp.svg'

Dir.glob("*svg") do |fname|
  puts fname
  #rebrand(fname, "RHEL7")
  system "inkscape --vacuum-defs -l ../getting-started/C/figures/#{fname} #{fname}"
end


