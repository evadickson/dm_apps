import statistics
import pandas
import unicodecsv as csv
import xlsxwriter as xlsxwriter
from django.http import HttpResponse
from django.template.defaultfilters import yesno
from math import pi

from bokeh.io import show, export_png, export_svgs
from bokeh.models import SingleIntervalTicker, ColumnDataSource, HoverTool, LabelSet, Label, Title
from bokeh.plotting import figure, output_file, save
from bokeh import palettes
from bokeh.transform import cumsum
from django.db.models import Sum, Q
from shutil import rmtree
from django.conf import settings

from lib.functions.nz import nz
from . import models
import numpy as np
import os
import pandas as pd


def generate_species_count_report(species_list):
    # start assigning files and by cleaning the temp dir
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, 'templates', 'camp', 'temp')
    target_file = os.path.join(target_dir, 'report_temp.html')

    try:
        rmtree(target_dir)
    except:
        print("no such dir.")
    os.mkdir(target_dir)

    # output to static HTML file
    output_file(target_file)

    # create a new plot
    title_eng = "Count of Species Observations by Year"

    p = figure(
        tools="pan,box_zoom,wheel_zoom,reset,save",
        x_axis_label='Year',
        y_axis_label='Count',
        plot_width=1200, plot_height=600,

    )

    p.add_layout(Title(text=title_eng, text_font_size="16pt"), 'above')


    # determine number of species
    # print(species_list)
    my_list = species_list.split(",")

    # prime counter variable
    i = 0

    # generate color palette
    if len(my_list) <= 2:
        colors = palettes.Set1[3][:len(my_list)]
    elif len(my_list) <= 9:
        colors = palettes.Set1[len(my_list)]
    else:
        colors = palettes.Category20[len(my_list)]

    for obj in my_list:
        sp_id = int(obj.replace("'", ""))
        # create a new file containing data
        qs = models.SpeciesObservation.objects.filter(species=sp_id).values(
            'sample__year'
        ).distinct().annotate(dsum=Sum('total_non_sav'))

        years = [i["sample__year"] for i in qs]
        counts = [i["dsum"] for i in qs]
        my_sp = models.Species.objects.get(pk=sp_id)
        legend_title = "Annual observations for {}".format(my_sp.common_name_eng)
        p.line(years, counts, legend=legend_title, line_color=colors[i], line_width=3)
        p.circle(years, counts, legend=legend_title, fill_color=colors[i], line_color=colors[i], size=8)
        i += 1

    save(p)


def generate_species_richness_report(site=None):
    # start assigning files and by cleaning the temp dir
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, 'templates', 'camp', 'temp')
    target_file = os.path.join(target_dir, 'report_temp.html')

    try:
        rmtree(target_dir)
    except:
        print("no such dir.")
    os.mkdir(target_dir)

    # output to static HTML file
    output_file(target_file)

    # create a new plot
    p = figure(
        title="Count of Species Observations by Year",
        tools="pan,box_zoom,wheel_zoom,reset,save,",
        # tooltips="@stations",
        x_axis_label='Year',
        y_axis_label='Species count',
        plot_width=1200, plot_height=800,
        x_axis_type="linear"

    )
    ticker = SingleIntervalTicker(interval=1)

    p.grid.grid_line_alpha = 1
    p.background_fill_color = None
    p.xaxis.minor_tick_line_color = None
    p.xaxis.ticker = ticker
    if site:
        # reset title
        p.title.text = "Count of Species Observations by Year - {}".format(models.Site.objects.get(pk=site))

        # first we need a list of stations
        stations = models.Station.objects.filter(site_id=site).order_by("name")

        # generate color palette
        if len(stations) <= 2:
            colors = palettes.Set1[3][:len(stations)]
        elif len(stations) <= 9:
            colors = palettes.Set1[len(stations)]
        else:
            colors = palettes.Category20[len(stations)]

        i = 0
        for station in stations:
            print(station)
            qs_years = models.Sample.objects.filter(station=station).order_by("year").values(
                'year',
            ).distinct()

            years = []
            counts = []

            for obj in qs_years:
                y = obj['year']
                annual_obs = models.SpeciesObservation.objects.filter(sample__year=y, sample__station=station,
                                                                      species__sav=False).values(
                    'species_id',
                ).distinct()
                species_set = set([i["species_id"] for i in annual_obs])
                years.append(y)
                counts.append(len(species_set))

            legend_title = str(station)

            source = ColumnDataSource(data={
                'year': years,
                'count': counts,
                'station': list(np.repeat(str(station), len(years)))
            })

            p.line("year", "count", legend=legend_title, line_width=1, line_color=colors[i], source=source)
            # p.circle("year", "count", legend=legend_title, line_width=1, line_color=colors[i], source=source)
            p.circle("year", "count", legend=legend_title, fill_color=colors[i], line_color=colors[i], size=3,
                     source=source)

            p.add_tools(HoverTool(
                tooltips=[
                    ('year:', '@year'),
                    ('station:', '@station'),  # use @{ } for field names with spaces
                    ('count:', '@count'),
                ],
            ))
            # increase the counter to move to next station
            i += 1

        # Show a line for entire site
        qs_years = models.Sample.objects.filter(station__site_id=site).order_by("year").values(
            'year',
        ).distinct()

        years = []
        counts = []

        for obj in qs_years:
            y = obj['year']
            annual_obs = models.SpeciesObservation.objects.filter(sample__year=y, sample__station__site_id=site,
                                                                  species__sav=False).values(
                'species_id',
            ).distinct()
            species_set = set([i["species_id"] for i in annual_obs])
            years.append(y)
            counts.append(len(species_set))

        legend_title = "Entire site"

        source = ColumnDataSource(data={
            'year': years,
            'count': counts,
            'station': list(np.repeat("all stations", len(years)))
        })

        p.line("year", "count", legend=legend_title, line_width=3, line_color='black', line_dash="4 4", source=source)
        p.circle("year", "count", legend=legend_title, fill_color='black', line_color="black", size=8, source=source)

        p.add_tools(HoverTool(
            tooltips=[
                ('year:', '@year'),
                ('station:', '@station'),  # use @{ } for field names with spaces
                ('count:', '@count'),
            ],
        ))

        # p.line(years, counts, legend=legend_title, line_width=3, line_color='black', line_dash="4 4")
        # p.circle(years, counts, legend=legend_title, fill_color='black', line_color='black', size=8)
        # TODO: should we show the number of stations visited?

    else:
        qs_years = models.Sample.objects.all().order_by("year").values(
            'year',
        ).distinct()

        years = []
        counts = []

        for obj in qs_years:
            y = obj['year']
            annual_obs = models.SpeciesObservation.objects.filter(sample__year=y, species__sav=False).values(
                'species_id',
            ).distinct()
            species_set = set([i["species_id"] for i in annual_obs])
            years.append(y)
            print(years)
            counts.append(len(species_set))
            print(counts)
        # my_sp = models.Species.objects.get(pk=sp_id)
        legend_title = "All stations"
        p.line(years, counts, legend=legend_title, line_width=3)
        p.circle(years, counts, legend=legend_title, fill_color='white', size=8)
        # TODO: should we show the number of stations visited?

    save(p)


WIDTH = 1200
HEIGHT = 800
TITLE_FONT_SIZE = '16pt'
LEGEND_FONT_SIZE = '12pt'


def generate_annual_watershed_report(site, year):
    # start assigning files and by cleaning the temp dir
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'camp', 'temp')
    target_file_pie = os.path.join(target_dir, 'pie_chart.png')
    target_file_richness = os.path.join(target_dir, 'species_richness.png')
    target_file_do = os.path.join(target_dir, 'do.png')
    target_file_greeb_crab = os.path.join(target_dir, 'green_crab.png')

    # try:
    #     rmtree(target_dir)
    # except:
    #     print("no such dir.")
    # os.mkdir(target_dir)

    generate_sub_pie_chart(site, year, target_file_pie)
    generate_sub_species_richness(site, target_file_richness)
    generate_sub_do(site, target_file_do)
    generate_sub_green_crab(site, target_file_greeb_crab)

    return None


def generate_sub_pie_chart(site, year, target_file):
    # species will be represented by percentages of the total number of species observed at a given site
    species_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, ]

    # create a dictionary of species codes by counts
    x = {}
    for s in species_list:
        s_code = models.Species.objects.get(pk=s).code
        s_sum = models.SpeciesObservation.objects.filter(sample__station__site_id=site).filter(
            sample__year=year).filter(
            species_id=s).order_by("species").values('species').distinct().annotate(
            dsum=Sum('total_non_sav'))
        try:
            x[s_code] = s_sum[0]["dsum"]
        except:
            x[s_code] = 0

    # now we need to add the 'other' category
    cum_mod = models.SpeciesObservation.objects.filter(sample__station__site_id=site).filter(sample__year=year)
    for s in species_list:
        s_code = 'Other'
        cum_mod = cum_mod.filter(~Q(species_id=s))

    cum_mod = cum_mod.order_by('sample__station__site_id').values('sample__station__site_id').distinct().annotate(
        dsum=Sum('total_non_sav'))
    try:
        x[s_code] = cum_mod[0]["dsum"]
    except:
        x[s_code] = 0

    # prepare the data for the glyph
    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'species'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['percentage'] = data['value'] / data['value'].sum()
    data['color'] = palettes.Category20[len(x)]
    data['legend_label'] = ["{} - {:.1%}".format(data['species'][i], data['percentage'][i]) for i in range(0, len(x))]

    site_name = str(models.Site.objects.get(pk=site))
    title_fre = "Les 13 espèces les plus communes et rares observées à {}, en {}".format(site_name, year)
    title_eng = "13 Most Common and Rare Species Observed in {} for {}".format(site_name, year)

    p = figure(plot_height=HEIGHT, plot_width=WIDTH, toolbar_location=None,
               x_range=(-0.5, 1.0), )
    p.add_layout(Title(text=title_fre, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_eng, text_font_size=TITLE_FONT_SIZE), 'above')

    p.wedge(x=0, y=0, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='legend_label', source=data)
    p.legend.label_text_font_size = LEGEND_FONT_SIZE
    total_mod = models.SpeciesObservation.objects.filter(sample__station__site_id=site).filter(
        sample__year=year).order_by('sample__station__site_id').values('sample__station__site_id').distinct().annotate(
        dsum=Sum('total_non_sav'))
    total_abundance = total_mod[0]["dsum"]
    citation = Label(x=0.45, y=-0.7,
                     text='Total abundance / abondance totale = {:,}'.format(total_abundance), render_mode='css',
                     border_line_color='black', border_line_alpha=1.0,
                     background_fill_color='white', background_fill_alpha=1.0)
    p.add_layout(citation)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    export_png(p, filename=target_file)
    return None


def generate_sub_species_richness(site, target_file):
    # create a new plot
    site_name = str(models.Site.objects.get(pk=site))
    title_fre = "Abondance d’espèces par année à {}".format(site_name)
    title_eng = "Species Richness by Year at {}".format(site_name)

    p = figure(
        x_axis_label='Year / année',
        y_axis_label="Species count / nombre d'espèces",
        plot_width=WIDTH, plot_height=HEIGHT,
        x_axis_type="linear",
        toolbar_location=None,

    )
    ticker = SingleIntervalTicker(interval=1)
    p.add_layout(Title(text=title_fre, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_eng, text_font_size=TITLE_FONT_SIZE), 'above')

    p.title.text_font_size = TITLE_FONT_SIZE
    p.grid.grid_line_alpha = 1
    p.background_fill_color = "white"
    p.xaxis.minor_tick_line_color = None
    p.xaxis.ticker = ticker

    # first we need a list of stations
    stations = models.Station.objects.filter(site_id=site).order_by("name")

    # generate color palette
    if len(stations) <= 10:
        colors = palettes.Category10[len(stations)]
    else:
        colors = palettes.Category20[len(stations)]

    i = 0
    for station in stations:
        qs_years = models.Sample.objects.filter(station=station).order_by("year").values(
            'year',
        ).distinct()

        years = []
        counts = []

        for obj in qs_years:
            y = obj['year']
            annual_obs = models.SpeciesObservation.objects.filter(sample__year=y, sample__station=station,
                                                                  species__sav=False).values(
                'species_id',
            ).distinct()
            species_set = set([i["species_id"] for i in annual_obs])
            years.append(y)
            counts.append(len(species_set))

        legend_title = str(station)

        source = ColumnDataSource(data={
            'year': years,
            'count': counts,
            'station': list(np.repeat(str(station), len(years)))
        })

        p.line("year", "count", legend=legend_title, line_width=1, line_color=colors[i], source=source)
        p.circle("year", "count", legend=legend_title, fill_color=colors[i], line_color=colors[i], size=3,
                 source=source)
        i += 1

    # Show a line for entire site
    qs_years = models.Sample.objects.filter(station__site_id=site).order_by("year").values(
        'year',
    ).distinct()

    years = []
    counts = []

    for obj in qs_years:
        y = obj['year']
        annual_obs = models.SpeciesObservation.objects.filter(sample__year=y, sample__station__site_id=site,
                                                              species__sav=False).values(
            'species_id',
        ).distinct()
        species_set = set([i["species_id"] for i in annual_obs])
        years.append(y)
        counts.append(len(species_set))

    legend_title = "Entire site / ensemble du site"

    source = ColumnDataSource(data={
        'year': years,
        'count': counts,
        'station': list(np.repeat("all stations", len(years)))
    })

    p.line("year", "count", legend=legend_title, line_width=3, line_color='black', line_dash="4 4", source=source)
    p.circle("year", "count", legend=legend_title, fill_color='black', line_color="black", size=8, source=source)
    p.legend.label_text_font_size = LEGEND_FONT_SIZE
    export_png(p, filename=target_file)


def generate_sub_do(site, target_file):
    # create a new plot
    site_name = str(models.Site.objects.get(pk=site))
    title_eng = "Dissolved Oxygen Levels per Year (Average) at {}".format(site_name)
    title_fre = "Niveaux d’oxygène dissous par année (moyenne) à {}".format(site_name)
    p = figure(
        x_axis_label='Year / année',
        y_axis_label='Dissolved oxygen / oxygène dissous (mg/l)',
        plot_width=WIDTH, plot_height=HEIGHT,
        x_axis_type="linear",
        toolbar_location=None,
    )
    ticker = SingleIntervalTicker(interval=1)
    p.add_layout(Title(text=title_fre, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_eng, text_font_size=TITLE_FONT_SIZE), 'above')

    p.grid.grid_line_alpha = 1
    p.background_fill_color = "white"
    p.xaxis.minor_tick_line_color = None
    p.xaxis.ticker = ticker

    # first we need a list of stations
    stations = models.Station.objects.filter(site_id=site).order_by("name")

    # generate color palette
    if len(stations) <= 10:
        colors = palettes.Category10[len(stations)]
    else:
        colors = palettes.Category20[len(stations)]

    i = 0
    for station in stations:
        qs_years = models.Sample.objects.filter(station=station).order_by("year").values(
            'year',
        ).distinct()

        years = []
        do_max = []
        do_min = []
        do_avg = []

        for obj in qs_years:
            y = obj['year']
            do_readings = [obj.dissolved_o2 for obj in models.Sample.objects.filter(year=y).filter(station=station)]
            do_readings = list(filter(None, do_readings))
            do_max.append(max(do_readings))
            do_min.append(min(do_readings))
            do_avg.append(statistics.mean(do_readings))
            years.append(y)
        legend_title = str(station)

        source = ColumnDataSource(data={
            'stations': list(np.repeat(str(station), len(years))),
            'years': years,
            'do_max': do_max,
            'do_min': do_min,
            'do_avg': do_avg,
        })

        p.segment("years", "do_max", "years", "do_min", color=colors[i], source=source)
        p.dash(x="years", y="do_max", size=15, color=colors[i], source=source)
        p.dash(x="years", y="do_min", size=15, color=colors[i], source=source)
        p.line("years", "do_avg", legend=legend_title, line_width=1, line_color=colors[i], source=source)
        p.circle("years", "do_avg", legend=legend_title, fill_color=colors[i], line_color=colors[i], size=3,
                 source=source)
        i += 1

    # show(p)
    p.legend.label_text_font_size = LEGEND_FONT_SIZE
    export_png(p, filename=target_file)


def generate_sub_green_crab(site, target_file):
    # create a new plot
    site_name = str(models.Site.objects.get(pk=site))
    title_eng = "Green Crab Abundance per Year at {}".format(site_name)
    title_fre = "Abondance du Crab vert, par année à {}".format(site_name)

    color = palettes.BuGn[5][2]

    years = [obj["year"] for obj in models.Sample.objects.order_by("year").values('year').distinct()]
    counts = []
    for year in years:
        green_crab_sum = models.SpeciesObservation.objects.filter(sample__station__site_id=site).filter(
            sample__year=year).filter(species_id=18).order_by("species").values('species').distinct().annotate(
            dsum=Sum('total_non_sav'))
        try:
            counts.append(green_crab_sum[0]["dsum"])
        except:
            counts.append(0)

    years = [str(y) for y in years]
    source = ColumnDataSource(data={
        'years': years,
        'counts': counts,
    })
    p = figure(
        x_range=years,
        toolbar_location=None,
        plot_width=WIDTH,
        plot_height=HEIGHT,
        x_axis_label='Year / année',
        y_axis_label='Abundance / Abondance',
    )
    p.vbar(x='years', top='counts', width=0.9, source=source, line_color='white', fill_color=color)
    p.add_layout(Title(text=title_fre, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_eng, text_font_size=TITLE_FONT_SIZE), 'above')

    labels = LabelSet(x='years', y='counts', text='counts', level='glyph',
                      x_offset=-10, y_offset=5, source=source, render_mode='canvas')
    p.add_layout(labels)

    # show(p)
    export_png(p, filename=target_file)


def generate_annual_watershed_spreadsheet(site, year):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'camp', 'temp')
    target_file = "temp_data_export.xlsx"
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'camp', 'temp', target_file)

    # get a sample list for the site / year
    sample_list = models.Sample.objects.filter(year=year).filter(station__site=site).order_by("start_date",
                                                                                              "station__station_number")
    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)
    worksheet1 = workbook.add_worksheet(name="Fauna - Faune")
    worksheet2 = workbook.add_worksheet(name="Sediment - Sédiment")
    worksheet3 = workbook.add_worksheet(name="Vegetation - Végétation")

    # spreadsheet: Fauna #
    ######################

    # get a list of species obs for which sav == false
    species_list = models.Species.objects.filter(sav=False).order_by("code")

    # convert species list into headers (a, yoy, tot)
    species_header_list = []
    for s in species_list:
        species_header_list.append("{}(A)".format(s.code))
        species_header_list.append("{}(YOY)".format(s.code))
        species_header_list.append("{}(TOT)".format(s.code))

    header_eng = [
        "Site location",
        "Station #",
        "Station name",
        "Date",
        "Month",
        "Year",
        "Time start",
        "Time finish",
        "Water Sample #",
        "Rain 24h Y / N",
        "Stage of tide",
        "Samplers name",
        "Water temp",
        "Salinity",
        "Dissolved Oxygen",
        "Water turbidity",
        "SP. RICHNESS",
        "TOTAL",
    ]

    header_fre = [
        "Location Site",
        "# Station",
        "Nom station",
        "(dj/mm/ya)",
        "Mois",
        "Année",
        "Heure début",
        "Heure fin",
        "# échantillon d'eau",
        "Pluie 24h O / N",
        "Stade de marée",
        "Nom échantillonneurs",
        "Temp eau",
        "Salinité",
        "Oxygène dissout",
        "Turbidité de l'eau",
        "SP. RICHNESS",
        "TOTAL",
    ]

    # insert species headers 2 from the last item in header_eng / fre
    header_eng[-2:-2] = species_header_list
    header_fre[-2:-2] = species_header_list

    # prime a dataframe obj with the two headers
    my_df = pandas.DataFrame([header_eng, header_fre], columns=[i for i in range(0, len(header_eng))])

    # write some data
    for s in sample_list:
        data_row = [
            s.station.site.site,
            s.station.station_number,
            s.station.name,
            s.start_date.strftime("%d/%m/%Y"),
            s.start_date.month,
            s.start_date.year,
            s.start_date.strftime("%H:%M"),
            s.end_date.strftime("%H:%M"),
            s.nutrient_sample_id,
            yesno(s.rain_past_24_hours),
            "{} - {}".format(s.get_tide_state_display(), s.get_tide_direction_display(), ),
            s.samplers,
            s.h2o_temperature_c,
            s.salinity,
            s.dissolved_o2,
            s.get_water_turbidity_display(),
        ]

        # now get species data
        species_obs_list = []

        for species in species_list:
            try:
                species_obs = models.SpeciesObservation.objects.get(sample=s, species=species)
            except:
                species_obs_list.append(0)
                species_obs_list.append(0)
                species_obs_list.append(0)
            else:
                nz(species_obs_list.append(species_obs.adults), 0)
                nz(species_obs_list.append(species_obs.yoy), 0)
                species_obs_list.append(species_obs.total_non_sav)

        data_row.extend(species_obs_list)

        # species richness
        annual_obs = models.SpeciesObservation.objects.filter(sample=s, species__sav=False).values(
            'species_id',
        ).distinct()
        species_set = set([i["species_id"] for i in annual_obs])
        data_row.append(len(species_set))

        # total count
        total = models.SpeciesObservation.objects.filter(sample=s).filter(species__sav=False).values(
            'sample_id'
        ).distinct().annotate(dsum=Sum('total_non_sav'))
        data_row.append(total[0]['dsum'])

        # store data_row in a dataframe
        my_df = my_df.append(pandas.DataFrame([data_row, ], columns=[i for i in range(0, len(data_row))]),
                             ignore_index=True)

    # create formatting
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#8C96A0', "align": 'center'})
    total_format = workbook.add_format({'bg_color': '#D6D1C0', "align": 'center'})
    normal_format = workbook.add_format({"align": 'center'})
    bold_format = workbook.add_format({"align": 'center', 'bold': True})

    # write dataframe to xlsx
    for i in range(0, my_df.shape[0]):
        for j in range(0, my_df.shape[1]):

            # tricky code since j and i are reverses from an intuitive perspective (i.e. not i,j)
            my_val = my_df[j][i]

            if i <= 1:
                worksheet1.write(i, j, my_val, header_format)
            elif "(TOT)" in my_df[j][0]:
                worksheet1.write(i, j, my_val, total_format)
            else:
                worksheet1.write(i, j, my_val, normal_format)

    # add the total at bottom right
    total_sum = 0
    count = 0
    for j in my_df[my_df.shape[1] - 1]:
        if count > 1:
            total_sum = total_sum + j
        count += 1
    worksheet1.write(my_df.shape[0], my_df.shape[1] - 2, "TOTAL", bold_format)
    worksheet1.write(my_df.shape[0], my_df.shape[1] - 1, total_sum, bold_format)

    # adjust the width of the columns based on the max string length in each col
    col_max = [max([len(str(s)) for s in my_df[j].values]) for j in my_df.columns]
    for j in my_df.columns:
        worksheet1.set_column(j, j, width=col_max[j] * 1.1)

    # spreadsheet: sediment #
    #########################

    # get a list of species obs for which sav == false
    species_list = models.Species.objects.filter(sav=False).order_by("code")

    for s in species_list:
        species_header_list.append("{}(A)".format(s.code))
        species_header_list.append("{}(YOY)".format(s.code))
        species_header_list.append("{}(TOT)".format(s.code))

    header_eng = [
        "Site location",
        "Station #",
        "Station name",
        "Date",
        "Month",
        "Year",
        "% sand",
        "% gravel",
        "% rocky",
        "% mud",
        "Overall visual sediment observation",
    ]

    header_fre = [
        "Location Site",
        "# Station",
        "Nom station",
        "(dj/mm/ya)",
        "Mois",
        "Année",
        "% sable",
        "% gravier",
        "% rocheux",
        "% vase",
        "Observation visuelle du sédiment",
    ]

    # create formatting
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#8C96A0', "align": 'center'})
    normal_format = workbook.add_format({"align": 'center'})

    # prime a dataframe obj with the two headers
    my_df = pandas.DataFrame([header_eng, header_fre], columns=[i for i in range(0, len(header_eng))])

    # write some data
    for s in sample_list:
        data_row = [
            s.station.site.site,
            s.station.station_number,
            s.station.name,
            s.start_date.strftime("%d/%m/%Y"),
            s.start_date.month,
            s.start_date.year,
            "{}%".format(nz(s.percent_sand, 0)),
            "{}%".format(nz(s.percent_gravel, 0)),
            "{}%".format(nz(s.percent_rock, 0)),
            "{}%".format(nz(s.percent_mud, 0)),
            "{}%".format(
                sum([nz(s.percent_sand, 0), nz(s.percent_gravel, 0), nz(s.percent_rock, 0), nz(s.percent_mud, 0)])),
        ]

        # store data_row in a dataframe
        my_df = my_df.append(pandas.DataFrame([data_row, ], columns=[i for i in range(0, len(data_row))]),
                             ignore_index=True)

    # write dataframe to xlsx
    for i in range(0, my_df.shape[0]):
        for j in range(0, my_df.shape[1]):

            # tricky code since j and i are reverses from an intuitive perspective (i.e. not i,j)
            my_val = my_df[j][i]

            if i <= 1:
                worksheet2.write(i, j, my_val, header_format)
            else:
                worksheet2.write(i, j, my_val, normal_format)

    # adjust the width of the columns based on the max string length in each col
    col_max = [max([len(str(s)) for s in my_df[j].values]) for j in my_df.columns]
    for j in my_df.columns:
        worksheet2.set_column(j, j, width=col_max[j] * 1.1)

    # spreadsheet: Veg #
    ####################

    # get a list of species obs for which sav == true
    species_list = models.Species.objects.filter(sav=True).order_by("code")

    # convert sav species list into headers (a, yoy, tot)
    species_header_list_eng = [s.common_name_eng for s in species_list]
    species_header_list_fre = [s.common_name_fre for s in species_list]

    header_eng = [
        "Site location",
        "Station #",
        "Station name",
        "Date",
        "Month",
        "Year",
    ]

    header_fre = [
        "Location Site",
        "# Station",
        "Nom station",
        "(dj/mm/ya)",
        "Mois",
        "Année",
    ]

    # insert species headers 2 from the last item in header_eng / fre
    header_eng.extend(species_header_list_eng)
    header_fre.extend(species_header_list_fre)

    # prime a dataframe obj with the two headers
    my_df = pandas.DataFrame([header_eng, header_fre], columns=[i for i in range(0, len(header_eng))])

    # write some data
    for s in sample_list:
        data_row = [
            s.station.site.site,
            s.station.station_number,
            s.station.name,
            s.start_date.strftime("%d/%m/%Y"),
            s.start_date.month,
            s.start_date.year,
        ]

        # now get species data
        species_obs_list = []

        for species in species_list:
            try:
                species_obs = models.SpeciesObservation.objects.get(sample=s, species=species)
            except:
                species_obs_list.append(0)
            else:
                species_obs_list.append(nz(species_obs.total_sav, 0))

        data_row.extend(species_obs_list)

        # store data_row in a dataframe
        my_df = my_df.append(pandas.DataFrame([data_row, ], columns=[i for i in range(0, len(data_row))]),
                             ignore_index=True)

    # create formatting
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#8C96A0', "align": 'center'})
    normal_format = workbook.add_format({"align": 'center'})

    # write dataframe to xlsx
    for i in range(0, my_df.shape[0]):
        for j in range(0, my_df.shape[1]):

            # tricky code since j and i are reverses from an intuitive perspective (i.e. not i,j)
            my_val = my_df[j][i]

            if i <= 1:
                worksheet3.write(i, j, my_val, header_format)
            else:
                worksheet3.write(i, j, my_val, normal_format)

    # adjust the width of the columns based on the max string length in each col
    col_max = [max([len(str(s)) for s in my_df[j].values]) for j in my_df.columns]
    for j in my_df.columns:
        worksheet3.set_column(j, j, width=col_max[j] * 1.1)

    workbook.close()
    return target_url


def generate_fgp_export():
    # figure out the filename
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fgp_dataset_for_camp.csv"'
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer = csv.writer(response)
    # write the header
    writer.writerow([
        "year / année",
        "month / mois",
        "province",
        "site",
        "station",
        "latitude (n)",
        "longitude (w)",
        "start date / date de début",
        "end date / date de fin",
        "ammonia / ammoniac",
        "dissolved oxygen / oxygène dissous",
        "nitrates",
        "nitrite",
        "phosphate",
        "salinity / salinité",
        "silicate",
        "water temperature / température de l'eau (C)",
        "gravel / gravier (%)",
        "mud / boue (%)",
        "rock / roche (%)",
        "sand / sable (%)",
        "species name (English) / nom de l'espèce (anglais)",
        "species name (French) / nom de l'espèce (français)",
        "scientific name / nom scientifique",
        "ITIS TSN ID",
        "submerged aquatic vegetation (SAV) / végétation aquatique submergée (VAS)",
        "SAV level observed / VAS niveau observé",
        "adults / adultes",
        "young of the year / jeune de l'année",
        "total number of individuals observed / total nombre d'individus observés",
    ])

    for obs in models.SpeciesObservation.objects.all():
        writer.writerow(
            [
                obs.sample.year,
                obs.sample.month,
                "{} - {}".format(obs.sample.station.site.province.province_eng, obs.sample.station.site.province.province_fre),
                obs.sample.station.site.site,
                obs.sample.station.name,
                obs.sample.station.latitude_n,
                obs.sample.station.longitude_w,
                obs.sample.start_date,
                obs.sample.end_date,
                obs.sample.ammonia,
                obs.sample.dissolved_o2,
                obs.sample.nitrates,
                obs.sample.nitrite,
                obs.sample.phosphate,
                obs.sample.salinity,
                obs.sample.silicate,
                obs.sample.h2o_temperature_c,
                obs.sample.percent_gravel,
                obs.sample.percent_mud,
                obs.sample.percent_rock,
                obs.sample.percent_sand,
                obs.species.common_name_eng,
                obs.species.common_name_fre,
                obs.species.scientific_name,
                obs.species.tsn,
                obs.species.sav,
                obs.adults,
                obs.yoy,
                obs.total_non_sav,
                obs.total_sav,
            ])
    return response

