# -*- coding: utf-8 -*-
# code provided as is without any liability to programmer. Use at your own risk!
# chris@navigato.com

#================================================================ index
def index():
    """ 
    Card Scan is a web-based app for gathering identification information from a USB card reader.    
    """    
    prog_succ = XML("40% Complete (success)")
    cla_only = SPAN(prog_succ,_class="sr-only")
    prog_bar = DIV(cla_only,_class="progress-bar progress-bar-success",_role="progressbar", aria={'valuenow':'20','valuemin':'0','valuemax':'100'}, _style="width: 20%")    
    prog_stripped = DIV(prog_bar,_class="progress progress-striped active")
    progress_bar = DIV(prog_stripped,_id="progress_bar")
    
    swipe_btn = SPAN(SPAN(_class="btn btn-default glyphicon glyphicon-credit-card"),_onclick='$("#display_license").html("");$("#progress_bar").show();$("#output_holder").focus();')
    output_holder = DIV(INPUT(_type="text", _name="output_holder",_size="5", _id="output_holder", _onchange="ajax('swipe_ajax',['output_holder'],'display_license');$('#output_holder').val('');$('#progress_bar').hide();"),_id="input_holder")
    return dict(action=DIV(swipe_btn,progress_bar),input_fragment=(output_holder))
    
def swipe_ajax():
    data = parse_card(request.vars.output_holder)
    license_builder = build_view(data)
    response.js = '$("#result_parse").draggable();' 
    return DIV(license_builder)
    

# meat and pototoes here:
def parse_card(swipe_data):
    import re 
    if len(swipe_data) < 100:
        return "Bad read, please try again"
    split_tracks = swipe_data.split('?') 
    if len(split_tracks) < 4:
        dirty_tracks = True
        return "Not certain that all the data was received, please try again"     
    alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    swipe_dict = {}
    swipe_dict['swipe_data'] = swipe_data
    swipe_dict['swipe_id'] = 'testing'
    swipe_dict['cdl_state'] = swipe_data[1:3] 
    zip_class = re.search(r'[?+!!](\d\d\d\d\d)\s+(\w+)\s',swipe_data) 
    swipe_dict['cdl_zipcode'] = zip_class.group(1)
    swipe_dict['cdl_class'] = zip_class.group(2)
    lic_date = re.search(r';(\d+)=(\d+)?',swipe_data)
    lic = lic_date.group(1)
    lic_num = lic[-7:]
    lic_alpha = lic[-9],lic[-8]
    lic_alpha = alphabet[int(''.join(lic_alpha))-1]
    swipe_dict['cdl_id'] =  lic_alpha + lic_num
    dates = lic_date.group(2)
    ex_yr = dates[0:2]
    dob_d = dates[10:]
    dob_m = dates[2:4]
    dob_yyyy = dates[4:8]
    swipe_dict['cdl_expires'] = dob_m + '/' + dob_d  + '/20' + ex_yr
    swipe_dict['cdl_dob'] = dob_m + '/' + dob_d  + '/' + dob_yyyy    
    me = re.search(r'\s([A-Z])(\d)(\d\d)(\d\d\d)([A-Z]+)',swipe_data)
    swipe_dict['cdl_sex'] = me.group(1)
    swipe_dict['cdl_h_ft'] = me.group(2)
    swipe_dict['cdl_h_in'] = me.group(3)
    swipe_dict['cdl_weight'] = me.group(4)
    swipe_dict['cdl_eyes'] = me.group(5)[3:]
    swipe_dict['cdl_hair'] = me.group(5)[0:3]    
    split_track1 = split_tracks[0].split('^')
    # hack IF the field seperator doesn't exist between city and last name
    if len(split_track1) <= 3:
        swipe_dict['cdl_city'] = swipe_data[3:16]
        name = split_track1[0][16:].split('$')
        swipe_dict['cdl_full_name'] = name
        swipe_dict['cdl_l_name'] = name[0]
        swipe_dict['cdl_f_name'] = name[1]
        swipe_dict['cdl_other_name'] = name[2:]
        swipe_dict['cdl_address'] = split_track1[1]
    else:       
        swipe_dict['cdl_city'] = split_track1[0][3:]
        name = split_track1[1].split('$')
        swipe_dict['cdl_full_name'] = name
        swipe_dict['cdl_l_name'] = name[0]
        swipe_dict['cdl_f_name'] = name[1]
        swipe_dict['cdl_other_name'] = name[2:]
        swipe_dict['cdl_address'] = split_track1[2]        
    return swipe_dict  
    
    
def build_view(swipe_data):
    expires = SPAN(XML("expires: %s" %  swipe_data['cdl_expires']),_id="expires")
    license = SPAN(XML(swipe_data['cdl_id']),_id="driver_license")
    lic_class = SPAN(XML("Class: %s" %  swipe_data['cdl_class']),_id="lic_class")
    fullname = SPAN(swipe_data['cdl_full_name'][1],XML(" "),swipe_data['cdl_full_name'][0],XML(" "),XML(', '.join(swipe_data['cdl_full_name'][2:])))
    first_name = swipe_data['cdl_f_name']
    last_name = swipe_data['cdl_l_name']
    other_names = swipe_data['cdl_other_name']
    address = swipe_data['cdl_address']
    c_s_z = SPAN(XML(swipe_data['cdl_city']),XML(', '),XML(swipe_data['cdl_state']),XML('  '),XML(swipe_data['cdl_zipcode']))
    contact = SPAN(fullname,XML('<br />'),address,XML('<br />'),c_s_z,_id="cdl_contact")
    eyes = SPAN(B(XML("EYES:")),swipe_data['cdl_eyes'])
    height = SPAN(B(XML("HT:")),XML(swipe_data['cdl_h_ft']),XML("-"),XML(swipe_data['cdl_h_in']))
    sex = SPAN(B(XML("SEX:")),XML(swipe_data['cdl_sex']))
    hair = SPAN(B(XML("HAIR:")),XML(swipe_data['cdl_hair']))
    weight = SPAN(B(XML("WT:")),XML(swipe_data['cdl_weight']))
    dob = SPAN(B(XML("DOB:")),XML(swipe_data['cdl_dob']),_style="color:red;")
    cdl_attrib = SPAN(sex,hair,eyes,XML("<br />"),height,weight,dob,_id="cdl_attrib")
    return_build = DIV(expires,license,lic_class,contact,cdl_attrib,_id="result_parse")    
    return return_build
    
    

    

