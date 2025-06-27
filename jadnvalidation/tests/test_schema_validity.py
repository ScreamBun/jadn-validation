
from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import XML


def test_metadata_validity(): 
    root = "Metadata"    
  
    j_schema = {
    "info": {
      "title": "JADN Metaschema",
      "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
      "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
      "license": "CC-BY-4.0",
      "exports": ["Metadata"],
      "config": {
        "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$"
      }
    },

    "types": [
      ["Schema", "Record", [], "Definition of a JADN package", [
        [1, "info", "Metadata", ["[0"], "Information about this package"],
        [2, "types", "Type", ["[1", "]-1"], "Types defined in this package"]
      ]],
      

      ["Metadata", "Map", [], "Information about this package", [
        [1, "package", "Namespace", [], "Unique name/version of this package"],
        [2, "version", "String", ["{1", "[0"], "Incrementing version within package"],
        [3, "title", "String", ["{1", "[0"], "Title"],
        [4, "description", "String", ["{1", "[0"], "Description"],
        [5, "comment", "String", ["{1", "[0"], "Comment"],
        [6, "copyright", "String", ["{1", "[0"], "Copyright notice"],
        [7, "license", "String", ["{1", "[0"], "SPDX licenseId of this package"],
        [8, "namespaces", "PrefixNS", ["[0", "]-1"], "Referenced packages"],
        [9, "exports", "TypeName", ["[0", "]-1"], "Roots of the type tree(s) in this package"],
        [10, "config", "Config", ["[0"], "Configuration variables"],
        [11, "jadn_version", "Namespace", ["[0"], "JADN Metaschema package"]
      ]],

      ["PrefixNs", "Array", [], "Prefix corresponding to a namespace IRI", [
        [1, "prefix", "NSID", [], "Namespace prefix string"],
        [2, "namespace", "Namespace", [], "Namespace IRI"]
      ]],

      ["Config", "Map", ["{1"], "Config vars override JADN defaults", [
        [1, "$MaxBinary", "Integer", ["y1", "[0"], "Package max octets, default = 255"],
        [2, "$MaxString", "Integer", ["y1", "[0"], "Package max characters, default = 255"],
        [3, "$MaxElements", "Integer", ["y1", "[0"], "Package max items/properties, default = 255"],
        [4, "$Sys", "String", ["{1", "}1", "[0"], "System character for TypeName, default = '.'"],
        [5, "$TypeName", "String", ["/regex", "[0"], "Default = ^[A-Z][-.A-Za-z0-9]{0,63}$"],
        [6, "$FieldName", "String", ["/regex", "[0"], "Default = ^[a-z][_A-Za-z0-9]{0,63}$"],
        [7, "$NSID", "String", ["/regex", "[0"], "Default = ^([A-Za-z][A-Za-z0-9]{0,7})?$"]
      ]],

      ["Namespace", "String", ["/uri"], "Unique name of a package"],

      ["NSID", "String", ["%^([A-Za-z][A-Za-z0-9]{0,7})?$"], "Namespace prefix matching $NSID"],

      ["TypeName", "String", ["%^[A-Z][-.A-Za-z0-9]{0,63}$"], "Name of a logical type"],

      ["FieldName", "String", ["%^[a-z][_A-Za-z0-9]{0,63}$"], "Name of a field in a structured type"],

      ["TypeRef", "String", [], "Reference to a type, matching ($NSID ':')? $TypeName"],

      ["Type", "Array", [], "", [
        [1, "type_name", "TypeName", [], ""],
        [2, "core_type", "JADN-Type-Enum", ["#JADN-Type"]],
        [3, "type_options", "Options", ["[0"], ""],
        [4, "type_description", "Description", ["[0"]],
        [5, "fields", "ArrayOf", ["*JADN-Type"]]
      ]],

      ["JADN-Type-Enum", "Enumerated", [], "", [
        [1, "Binary"],
        [2, "Boolean"],
        [3, "Integer"],
        [4, "Number"],
        [5, "String"],
        [6, "Enumerated"],
        [7, "Choice"],
        [8, "Array"],
        [9, "ArrayOf"],
        [10, "Map"],
        [11, "MapOf"],
        [12, "Record"]
      ]],

      ["JADN-Type", "Choice", [], "", [
        [1, "Binary", "Empty", [], ""],
        [2, "Boolean", "Empty", [], ""],
        [3, "Integer", "Empty", [], ""],
        [4, "Number", "Empty", [], ""],
        [5, "String", "Empty", [], ""],
        [6, "Enumerated", "Items", [], ""],
        [7, "Choice", "Fields", [], ""],
        [8, "Array", "Fields", [], ""],
        [9, "ArrayOf", "Empty", [], ""],
        [10, "Map", "Fields", [], ""],
        [11, "MapOf", "Empty", [], ""],
        [12, "Record", "Fields", [], ""]
      ]],

      ["Empty", "Array", ["}0"], "", []],

      ["Items", "ArrayOf", ["*Item"]],

      ["Fields", "ArrayOf", ["*Field"]],

      ["Item", "Array", [], "", [
        [1, "item_id", "FieldID"],
        [2, "item_value", "String"],
        [3, "item_description", "Description", ["[0"]]
      ]],

      ["Field", "Array", [], "", [
        [1, "field_id", "FieldID"],
        [2, "field_name", "FieldName"],
        [3, "field_type", "TypeRef"],
        [4, "field_options", "Options", ["[0"]],
        [5, "field_description", "Description", ["[0"]]
      ]],

      ["FieldID", "Integer", ["y0"]],

      ["Options", "ArrayOf", ["*Option"]],

      ["Option", "String", ["{1"]],

      ["Description", "String"]
    ]
  }
    
    valid_data = {
    "package": "http://example.fake",
    "exports": "Record-Name"
  }

    
    
    valid_data_list = [ valid_data ]
    invalid_data_list = [

         {'SuitEnum': 10},'Aces', 10
         
         ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_total_validity(): 
    root = "Schema"    
  
    j_schema = {
    "info": {
      "title": "JADN Metaschema",
      "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
      "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
      "license": "CC-BY-4.0",
      "exports": ["Metadata"],
      "config": {
        "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$"
      }
    },

    "types": [
      ["Schema", "Record", [], "Definition of a JADN package", [
        [1, "info", "String", ["[0"], "Information about this package"],
        [2, "types", "Type", ["[1", "]-1"], "Types defined in this package"]
      ]],
      

      ["Metadata", "Map", [], "Information about this package", [
        [1, "package", "Namespace", [], "Unique name/version of this package"],
        [2, "version", "String", ["{1", "[0"], "Incrementing version within package"],
        [3, "title", "String", ["{1", "[0"], "Title"],
        [4, "description", "String", ["{1", "[0"], "Description"],
        [5, "comment", "String", ["{1", "[0"], "Comment"],
        [6, "copyright", "String", ["{1", "[0"], "Copyright notice"],
        [7, "license", "String", ["{1", "[0"], "SPDX licenseId of this package"],
        [8, "namespaces", "PrefixNS", ["[0", "]-1"], "Referenced packages"],
        [9, "exports", "TypeName", ["[0", "]-1"], "Roots of the type tree(s) in this package"],
        [10, "config", "Config", ["[0"], "Configuration variables"],
        [11, "jadn_version", "Namespace", ["[0"], "JADN Metaschema package"]
      ]],

      ["PrefixNs", "Array", [], "Prefix corresponding to a namespace IRI", [
        [1, "prefix", "NSID", [], "Namespace prefix string"],
        [2, "namespace", "Namespace", [], "Namespace IRI"]
      ]],

      ["Config", "Map", ["{1"], "Config vars override JADN defaults", [
        [1, "$MaxBinary", "Integer", ["y1", "[0"], "Package max octets, default = 255"],
        [2, "$MaxString", "Integer", ["y1", "[0"], "Package max characters, default = 255"],
        [3, "$MaxElements", "Integer", ["y1", "[0"], "Package max items/properties, default = 255"],
        [4, "$Sys", "String", ["{1", "}1", "[0"], "System character for TypeName, default = '.'"],
        [5, "$TypeName", "String", ["/regex", "[0"], "Default = ^[A-Z][-.A-Za-z0-9]{0,63}$"],
        [6, "$FieldName", "String", ["/regex", "[0"], "Default = ^[a-z][_A-Za-z0-9]{0,63}$"],
        [7, "$NSID", "String", ["/regex", "[0"], "Default = ^([A-Za-z][A-Za-z0-9]{0,7})?$"]
      ]],

      ["Namespace", "String", ["/uri"], "Unique name of a package"],

      ["NSID", "String", ["%^([A-Za-z][A-Za-z0-9]{0,7})?$"], "Namespace prefix matching $NSID"],

      ["TypeName", "String", ["%^[A-Z][-.A-Za-z0-9]{0,63}$"], "Name of a logical type"],

      ["FieldName", "String", ["%^[a-z][_A-Za-z0-9]{0,63}$"], "Name of a field in a structured type"],

      ["TypeRef", "String", [], "Reference to a type, matching ($NSID ':')? $TypeName"],

      ["Type", "Array", [], "", [
        [1, "type_name", "TypeName", [], ""],
        [2, "core_type", "JADN-Type-Enum", []],
        [3, "type_options", "Options", ["[0"], ""],
        [4, "type_description", "Description", ["[0"]],
        [5, "fields", "ArrayOf", ["*JADN-Type", "[0"]]
      ]],

      ["JADN-Type-Enum", "Enumerated", [], "", [
        [1, "Binary"],
        [2, "Boolean"],
        [3, "Integer"],
        [4, "Number"],
        [5, "String"],
        [6, "Enumerated"],
        [7, "Choice"],
        [8, "Array"],
        [9, "ArrayOf"],
        [10, "Map"],
        [11, "MapOf"],
        [12, "Record"]
      ]],

      ["JADN-Type", "Choice", [], "", [
        [1, "Binary", "Empty", [], ""],
        [2, "Boolean", "Empty", [], ""],
        [3, "Integer", "Empty", [], ""],
        [4, "Number", "Empty", [], ""],
        [5, "String", "Empty", [], ""],
        [6, "Enumerated", "Items", [], ""],
        [7, "Choice", "Fields", [], ""],
        [8, "Array", "Fields", [], ""],
        [9, "ArrayOf", "Empty", [], ""],
        [10, "Map", "Fields", [], ""],
        [11, "MapOf", "Empty", [], ""],
        [12, "Record", "Fields", [], ""]
      ]],

      ["Empty", "Array", ["}0"], "", []],

      ["Items", "ArrayOf", ["*Item"]],

      ["Fields", "ArrayOf", ["*Field"]],

      ["Item", "Array", [], "", [
        [1, "item_id", "FieldID"],
        [2, "item_value", "String"],
        [3, "item_description", "Description", ["[0"]]
      ]],

      ["Field", "Array", [], "", [
        [1, "field_id", "FieldID"],
        [2, "field_name", "FieldName"],
        [3, "field_type", "TypeRef"],
        [4, "field_options", "Options", ["[0"]],
        [5, "field_description", "Description", ["[0"]]
      ]],

      ["FieldID", "Integer", ["y0"]],

      ["Options", "ArrayOf", ["*Option"]],

      ["Option", "String", ["{1"]],

      ["Description", "String"]
    ]
  }
    
    
    valid_data_list = [ 
        {
          "info" : "Hello, World",
          "types": ["String-Name", "String"]
        }
    ]
    invalid_data_list = [

         {'SuitEnum': 10},'Aces', 10
         
         ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 


"""
def test_types_validity(): 
    root = "Type"    
  
    j_schema = {
    "info": {
      "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
      "exports": ["Types-Map"],
      "config": {
        "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$"
      }
    },
    "types": [
      ["Types-Map", "MapOf", ["+String", "*Type-Array"], "TODO REMOVE THIS AND MERGE BACK INTO ONE DOC", []],
      ["Type-Array", "ArrayOf", ["*Type"], "TODO REMOVE THIS AND MERGE BACK INTO ONE DOC", []],
      ["Type", "Array", [], "", [
        [1, "type_name", "String"],
        [2, "core_type", "String"]
      ]],

    ]
  }
    
    valid_data_1 = {"types": [["Record-Name", "Record", [], "", [
        {"Fields": [1, "field_value_1", "String", [], ""]},
        {"Fields": [2, "field_value_2", "Integer", [], ""]}
      ]]]}
    valid_data_2 = {"types": [["String-Name", "String", [], "", {"String":[]}]]}
    valid_data_3 = {"types": [["String-Name", "String", {"String": ["Hello-World"]}]]}
    
    valid_data_4 = {"types": [["String-Name", "String", []]]}
    
    valid_data_list = [
    {
    "types" : [["String-Name", "String"]]
    }, 
    ["String-Name", "String"]
    ]

    #valid_data_list = [ valid_data_1, valid_data_2, valid_data_3, valid_data_4 ]
    invalid_data_list = [

         {'SuitEnum': 10},'Aces', 10
         
         ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 
    

  


{
  "info": {
    "title": "Music Library",
    "package": "http://fake-audio.org/music-lib",
    "version": "1.1",
    "description": "This information model defines a library of audio tracks, organized by album, with associated metadata regarding each track. It is modeled on the types of library data maintained by common websites and music file tag editors.",
    "license": "CC0-1.0",
    "exports": ["Library"]
  },
  "types": [
    ["Library", "MapOf", ["+Barcode", "*Album", "{1"], "Top level of the library is a map of CDs by barcode", []],
    ["Barcode", "String", ["%^\\d{12}$"], "A UPC-A barcode is 12 digits", []],
    ["Album", "Record", [], "model for the album", [
        [1, "album_artist", "Artist", [], "primary artist associated with this album"],
        [2, "album_title", "String", [], "publisher's title for this album"],
        [3, "pub_data", "Publication-Data", [], "metadata about the album's publication"],
        [4, "tracks", "Track", ["]0"], "individual track descriptions and content"],
        [5, "total_tracks", "Integer", ["{1"], "total track count"],
        [6, "cover_art", "Image", ["[0"], "cover art image for this album"]
      ]],
    ["Publication-Data", "Record", [], "who and when of publication", [
        [1, "publisher", "String", [], "record label that released this album"],
        [2, "release_date", "String", ["/date"], "and when did they let this drop"]
      ]],
    ["Image", "Record", [], "pretty picture for the album or track", [
        [1, "image_format", "Image-Format", [], "what type of image file?"],
        [2, "image_content", "Binary", [], "the image data in the identified format"]
      ]],
    ["Image-Format", "Enumerated", [], "can only be one, but can extend list", [
        [1, "PNG", ""],
        [2, "JPG", ""],
        [3, "GIF", ""]
      ]],
    ["Artist", "Record", [], "interesting information about a performer", [
        [1, "artist_name", "String", [], "who is this person"],
        [2, "instruments", "Instrument", ["q", "]0"], "and what do they play"]
      ]],
    ["Instrument", "Enumerated", [], "collection of instruments (non-exhaustive)", [
        [1, "vocals", ""],
        [2, "guitar", ""],
        [3, "bass", ""],
        [4, "drums", ""],
        [5, "keyboards", ""],
        [6, "percussion", ""],
        [7, "brass", ""],
        [8, "woodwinds", ""],
        [9, "harmonica", ""]
      ]],
    ["Track", "Record", [], "for each track there's a file with the audio and a metadata record", [
        [1, "location", "File-Path", [], "path to the audio file location in local storage"],
        [2, "metadata", "Track-Info", [], "description of the track"]
      ]],
    ["Track-Info", "Record", [], "information about the individual audio tracks", [
        [1, "track_number", "Integer", ["[1"], "track sequence number"],
        [2, "title", "String", [], "track title"],
        [3, "length", "Integer", ["{1"], "length of track in seconds; anticipated user display is mm:ss; minimum length is 1 second"],
        [4, "audio_format", "Audio-Format", [], "format of the digital audio"],
        [5, "featured_artist", "Artist", ["q", "[0", "]0"], "notable guest performers"],
        [6, "track_art", "Image", ["[0"], "each track can have optionally have individual artwork"],
        [7, "genre", "Genre", [], ""]
      ]],
    ["Audio-Format", "Enumerated", [], "can only be one, but can extend list", [
        [1, "MP3", ""],
        [2, "OGG", ""],
        [3, "FLAC", ""],
        [4, "MP4", ""],
        [5, "AAC", ""],
        [6, "WMA", ""],
        [7, "WAV", ""]
      ]],
    ["Genre", "Enumerated", [], "Enumeration of common genres", [
        [1, "rock", ""],
        [2, "jazz", ""],
        [3, "hip_hop", ""],
        [4, "electronic", ""],
        [5, "folk_country_world", ""],
        [6, "classical", ""],
        [7, "spoken_word", ""]
      ]],
    ["File-Path", "String", [], "local storage location of file with directory path from root, filename, and extension"]
  ]
}, 

  "types": [
    ["Record-Name", "Record", [], "", [
        [1, "field_value_1", "String", [], ""],
        [2, "field_value_2", "Integer", [], ""]
      ]]
  ]
"""