
from jadnvalidation.data_validation.data_validation import DataValidation
from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import XML


def test_metadata_validity(): 
    root = "Metadata"    
  
    j_schema = {
    "meta": {
      "title": "JADN Metaschema",
      "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
      "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
      "license": "CC-BY-4.0",
      "roots": ["Metadata"],
      "config": {
        "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$"
      }
    },

    "types": [
      ["Schema", "Record", [], "Definition of a JADN package", [
        [1, "meta", "Metadata", ["[0"], "Information about this package"],
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
        [9, "roots", "TypeName", ["[0", "]-1"], "Roots of the type tree(s) in this package"],
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
    "roots": ["Record-Name"]
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
    "meta": {
      "title": "JADN Metaschema",
      "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
      "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
      "license": "CC-BY-4.0",
      "roots": ["Schema"],
      "config": {
        "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$"
      }
    },
        "types": [
            
            ["Schema", "Record", [], "", [
                [1, "info", "String", [], ""],
                [2, "types", "String", ["[1", "]-1"], ""]]]
        ]}
      
    valid_data_list = [
        {
            "info" : "package",
            "types" : ["Typename2"]       
        }]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0

def test_total_validity(): 
    root = "Schema"    
  
    j_schema = {
    "meta": {
      "title": "JADN Metaschema",
      "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
      "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
      "license": "CC-BY-4.0",
      "roots": ["Schema"],
      "config": {
        "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$"
      }
    },

    "types": [
      ["Schema", "Record", [], "Definition of a JADN package", [
        [1, "meta", "Metadata", ["[0"], "Information about this package"],
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
        [9, "roots", "TypeName", ["[0", "]-1"], "Roots of the type tree(s) in this package"],
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
        [2, "core_type", "Enumerated", ["#JADN-Type"], ""],
        [3, "type_options", "Options", ["[0"], ""],
        [4, "type_description", "Description", ["[0"], ""],
        [5, "fields", "JADN-Type", ["[0", "&2"], ""]
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

      ["Items", "ArrayOf", ["*Item"], ""],

      ["Fields", "ArrayOf", ["*Field"], ""],

      ["Item", "Array", [], "", [
        [1, "item_id", "FieldID", [], ""],
        [2, "item_value", "String", [], ""],
        [3, "item_description", "Description", ["[0"], ""]
      ]],

      ["Field", "Array", [], "", [
        [1, "field_id", "FieldID", [], ""],
        [2, "field_name", "FieldName", [], ""],
        [3, "field_type", "TypeRef", [], ""],
        [4, "field_options", "Options", ["[0"], ""],
        [5, "field_description", "Description", ["[0"], ""]
      ]],

      ["FieldID", "Integer", ["y0"], ""],

      ["Options", "ArrayOf", ["*Option"], ""],

      ["Option", "String", ["{1"], ""],

      ["Description", "String", [], ""]
    ]
  }
    
    
    valid_data_list = [            
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Binary", [], ""]]        
        },        
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "String", ["[0"], "", []]]        
        },             
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Integer", ["[0"], "", []]]        
        },          
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Number", ["[0"], "", []]]        
        },    
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Array", [], "", [
                [1, "thing", "String", [], ""]]

            ]]        
        },      
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Record", [], "", [
                [1, "thing", "String", [], ""]]
            ]]        
        },      
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Map", [], "", [
                [1, "thing", "String", [], ""]]

            ]]        
        },      
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "ArrayOf", ["*String"], ""

            ]]        
        },      
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "MapOf", ["+Integer", "*String"], ""

            ]]        
        },

        {
  "meta": {
    "title": "Music Library",
    "package": "http://fake-audio.org/music-lib",
    "version": "1.1",
    "description": "This information model defines a library of audio tracks, organized by album, with associated metadata regarding each track. It is modeled on the types of library data maintained by common websites and music file tag editors.",
    "license": "CC0-1.0",
    "roots": ["Library"]
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
def test_with_options():
    root = "Schema"    
  
    j_schema = {
        "meta": {
          "title": "JADN Metaschema",
          "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
          "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
          "license": "CC-BY-4.0",
          "roots": ["Schema"],
          "config": {
            "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$"
          }
        },
    "meta": {
      "title": "JADN Metaschema",
      "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
      "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
      "license": "CC-BY-4.0",
      "roots": ["Schema"],
      "config": {
        "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$"
      }
    },
        "types": [
          ["Schema", "Record", [], "Definition of a JADN package", [
            [1, "meta", "Metadata", ["[0"], "Information about this package"],
            [2, "types", "Type", ["]-1"], "Types defined in this package"]
          ]],
          ["Metadata", "Map", [], "Information about this package", [
            [1, "package", "Namespace", [], "Unique name/version of this package"],
            [2, "version", "String", ["{1", "[0"], "Incrementing version within package"],
            [3, "title", "String", ["{1", "[0"], "Title"],
            [4, "description", "String", ["{1", "[0"], "Description"],
            [5, "comment", "String", ["{1", "[0"], "Comment"],
            [6, "copyright", "String", ["{1", "[0"], "Copyright notice"],
            [7, "license", "String", ["{1", "[0"], "SPDX licenseId of this package"],
            [8, "namespaces", "PrefixNs", ["[0", "]-1"], "Referenced packages"],
            [9, "roots", "TypeName", ["[0", "]-1"], "Roots of the type tree(s) in this package"],
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
            [1, "type_name", "TypeName"],
            [2, "core_type", "Enumerated", ["#JADN-Type"]],
            [3, "type_options", "TypeOptions", ["[0", "&2"]],
            [4, "type_description", "Description", ["[0"]],
            [5, "fields", "JADN-Type", ["[0", "&2"]]
          ]],
          ["JADN-Type", "Choice", [], "", [
            [1, "Binary", "Empty"],
            [2, "Boolean", "Empty"],
            [3, "Integer", "Empty"],
            [4, "Number", "Empty"],
            [5, "String", "Empty"],
            [6, "Enumerated", "Items"],
            [7, "Choice", "Fields"],
            [8, "Array", "Fields"],
            [9, "ArrayOf", "Empty"],
            [10, "Map", "Fields"],
            [11, "MapOf", "Empty"],
            [12, "Record", "Fields"]
          ]],
          ["TypeOptions", "Choice", [], "", [
            [1, "Binary", "BinaryOpts"],
            [2, "Boolean", "BooleanOpts"],
            [3, "Integer", "IntegerOpts"],
            [4, "Number", "NumberOpts"],
            [5, "String", "StringOpts"],
            [6, "Enumerated", "EnumeratedOpts"],
            [7, "Choice", "ChoiceOpts"],
            [8, "Array", "ArrayOpts"],
            [9, "ArrayOf", "ArrayOfOpts"],
            [10, "Map", "MapOpts"],
            [11, "MapOf", "MapOfOpts"],
            [12, "Record", "RecordOpts"]
          ]],
          ["FieldOptions", "Choice", [], "", [
            [1, "Binary", "BinaryFieldOpts"],
            [2, "Boolean", "BooleanFieldOpts"],
            [3, "Integer", "IntegerFieldOpts"],
            [4, "Number", "NumberFieldOpts"],
            [5, "String", "StringFieldOpts"],
            [6, "Enumerated", "EnumeratedFieldOpts"],
            [7, "Choice", "ChoiceFieldOpts"],
            [8, "Array", "ArrayFieldOpts"],
            [9, "ArrayOf", "ArrayOfFieldOpts"],
            [10, "Map", "MapFieldOpts"],
            [11, "MapOf", "MapOfFieldOpts"],
            [12, "Record", "RecordFieldOpts"]
          ]],
          ["Empty", "Array", ["}0"]],
          ["Items", "ArrayOf", ["*Item"]],
          ["Fields", "ArrayOf", ["*Field"]],
          ["Item", "Array", [], "", [
            [1, "item_id", "FieldID"],
            [2, "item_value", "String", ["[0"]],
            [3, "item_description", "Description", ["[0"]]
          ]],
          ["Field", "Array", [], "", [
            [1, "field_id", "FieldID"],
            [2, "field_name", "FieldName"],
            [3, "field_type", "TypeRef"],
            [4, "field_options", "FieldOptions", ["[0", "&3"]],
            [5, "field_description", "Description", ["[0"]]
          ]],
          ["FieldID", "Integer", ["y0"]],
          ["Format", "String", ["%^/[a-zA-Z0-9]{1,16}+$"]],
          ["Description", "String"],
          ["AllOpts", "Array", [], "", [
            [1, "nillable", "Boolean", ["[0"]],
            [2, "abstract", "Boolean", ["[0"]],
            [3, "extends", "TypeRef", ["[0"]],
            [4, "restricts", "TypeRef", ["[0"]],
            [5, "final", "Boolean", ["[0"]]
            ]],
          ["FieldOptions", "Array", ["eAllOpts"], "", [
            [1, "nillable", "Boolean", ["[0"]],
            [2, "abstract", "Boolean", ["[0"]],
            [3, "extends", "TypeRef", ["[0"]],
            [4, "restricts", "TypeRef", ["[0"]],
            [5, "final", "Boolean", ["[0"]],
            [6, "minOccurs", "Integer", ["y0", "[0"]],
            [7, "maxOccurs", "Integer", ["y-2", "[0"]],
            [8, "tagId", "Integer", ["[0"]],
            [9, "key", "Boolean", ["[0"]],
            [10, "link", "Boolean", ["[0"]],
            [11, "not", "Boolean", ["[0"]]
          ]],
          ["BinaryOpts", "Array", ["eAllOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "nillable", "Boolean", ["[0"]],
            [3, "minLength", "Integer", ["[0"]],
            [4, "maxLength", "Integer", ["[0"]],
            [5, "default", "Binary", ["[0"]],
            [6, "const", "Binary", ["[0"]],
            [7, "attr", "Boolean", ["[0"]],
            [8, "abstract", "Boolean", ["[0"]],
            [9, "extends", "TypeRef", ["[0"]],
            [10, "restricts", "TypeRef", ["[0"]],
            [11, "final", "Boolean", ["[0"]],
            [12, "nillable", "Boolean", ["[0"]],
            [13, "abstract", "Boolean", ["[0"]],
            [14, "extends", "TypeRef", ["[0"]],
            [15, "restricts", "TypeRef", ["[0"]],
            [16, "final", "Boolean", ["[0"]]
          ]],
          ["BinaryFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "nillable", "Boolean", ["[0"]],
            [3, "minLength", "Integer", ["[0"]],
            [4, "maxLength", "Integer", ["[0"]],
            [5, "default", "Binary", ["[0"]],
            [6, "const", "Binary", ["[0"]],
            [7, "attr", "Boolean", ["[0"]],
            [8, "abstract", "Boolean", ["[0"]],
            [9, "extends", "TypeRef", ["[0"]],
            [10, "restricts", "TypeRef", ["[0"]],
            [11, "final", "Boolean", ["[0"]],
            [12, "nillable", "Boolean", ["[0"]],
            [13, "abstract", "Boolean", ["[0"]],
            [14, "extends", "TypeRef", ["[0"]],
            [15, "restricts", "TypeRef", ["[0"]],
            [16, "final", "Boolean", ["[0"]],
            [17, "minOccurs", "Integer", ["y0", "[0"]],
            [18, "maxOccurs", "Integer", ["y-2", "[0"]],
            [19, "tagId", "Integer", ["[0"]],
            [20, "key", "Boolean", ["[0"]],
            [21, "link", "Boolean", ["[0"]],
            [22, "not", "Boolean", ["[0"]]
          ]],
          ["BooleanOpts", "Array", ["eAllOpts"], "", [
            [1, "default", "Boolean", ["[0"]],
            [2, "const", "Boolean", ["[0"]],
            [3, "attr", "Boolean", ["[0"]],
            [4, "nillable", "Boolean", ["[0"]],
            [5, "abstract", "Boolean", ["[0"]],
            [6, "extends", "TypeRef", ["[0"]],
            [7, "restricts", "TypeRef", ["[0"]],
            [8, "final", "Boolean", ["[0"]]
          ]],
          ["BooleanFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "default", "Boolean", ["[0"]],
            [2, "const", "Boolean", ["[0"]],
            [3, "attr", "Boolean", ["[0"]],
            [4, "nillable", "Boolean", ["[0"]],
            [5, "abstract", "Boolean", ["[0"]],
            [6, "extends", "TypeRef", ["[0"]],
            [7, "restricts", "TypeRef", ["[0"]],
            [8, "final", "Boolean", ["[0"]],
            [91, "minOccurs", "Integer", ["y0", "[0"]],
            [93, "maxOccurs", "Integer", ["y-2", "[0"]],
            [38, "tagId", "Integer", ["[0"]],
            [75, "key", "Boolean", ["[0"]],
            [76, "link", "Boolean", ["[0"]],
            [78, "not", "Boolean", ["[0"]]
          ]],
          ["IntegerOpts", "Array", ["eAllOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minInclusive", "Integer", ["[0"]],
            [3, "maxInclusive", "Integer", ["[0"]],
            [4, "minExclusive", "Integer", ["[0"]],
            [5, "maxExclusive", "Integer", ["[0"]],
            [6, "default", "Integer", ["[0"]],
            [7, "const", "Integer", ["[0"]],
            [8, "attr", "Boolean", ["[0"]],
            [9, "nillable", "Boolean", ["[0"]],
            [10, "abstract", "Boolean", ["[0"]],
            [11, "extends", "TypeRef", ["[0"]],
            [12, "restricts", "TypeRef", ["[0"]],
            [13, "final", "Boolean", ["[0"]]
          ]],
          ["IntegerFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minInclusive", "Integer", ["[0"]],
            [3, "maxInclusive", "Integer", ["[0"]],
            [4, "minExclusive", "Integer", ["[0"]],
            [5, "maxExclusive", "Integer", ["[0"]],
            [6, "default", "Integer", ["[0"]],
            [7, "const", "Integer", ["[0"]],
            [8, "attr", "Boolean", ["[0"]],
            [9, "nillable", "Boolean", ["[0"]],
            [10, "abstract", "Boolean", ["[0"]],
            [11, "extends", "TypeRef", ["[0"]],
            [12, "restricts", "TypeRef", ["[0"]],
            [13, "final", "Boolean", ["[0"]],
            [14, "minOccurs", "Integer", ["y0", "[0"]],
            [15, "maxOccurs", "Integer", ["y-2", "[0"]],
            [16, "tagId", "Integer", ["[0"]],
            [17, "key", "Boolean", ["[0"]],
            [18, "link", "Boolean", ["[0"]],
            [19, "not", "Boolean", ["[0"]]
          ]],
          ["NumberOpts", "Array", ["eAllOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minInclusive", "Number", ["[0"]],
            [3, "maxInclusive", "Number", ["[0"]],
            [4, "minExclusive", "Number", ["[0"]],
            [5, "maxExclusive", "Number", ["[0"]],
            [6, "default", "Number", ["[0"]],
            [7, "const", "Number", ["[0"]],
            [8, "attr", "Boolean", ["[0"]],
            [9, "nillable", "Boolean", ["[0"]],
            [10, "abstract", "Boolean", ["[0"]],
            [11, "extends", "TypeRef", ["[0"]],
            [12, "restricts", "TypeRef", ["[0"]],
            [13, "final", "Boolean", ["[0"]]
          ]],
          ["NumberFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minInclusive", "Number", ["[0"]],
            [3, "maxInclusive", "Number", ["[0"]],
            [4, "minExclusive", "Number", ["[0"]],
            [5, "maxExclusive", "Number", ["[0"]],
            [6, "default", "Number", ["[0"]],
            [7, "const", "Number", ["[0"]],
            [8, "attr", "Boolean", ["[0"]],
            [9, "nillable", "Boolean", ["[0"]],
            [10, "abstract", "Boolean", ["[0"]],
            [11, "extends", "TypeRef", ["[0"]],
            [12, "restricts", "TypeRef", ["[0"]],
            [13, "final", "Boolean", ["[0"]],
            [14, "minOccurs", "Integer", ["y0", "[0"]],
            [15, "maxOccurs", "Integer", ["y-2", "[0"]],
            [16, "tagId", "Integer", ["[0"]],
            [17, "key", "Boolean", ["[0"]],
            [18, "link", "Boolean", ["[0"]],
            [19, "not", "Boolean", ["[0"]]
          ]],
          ["StringOpts", "Array", ["eAllOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minInclusive", "String", ["[0"]],
            [3, "maxInclusive", "String", ["[0"]],
            [4, "minExclusive", "String", ["[0"]],
            [5, "maxExclusive", "String", ["[0"]],
            [6, "pattern", "String", ["/regex", "[0"]],
            [7, "minLength", "Integer", ["y0", "[0"]],
            [8, "maxLength", "Integer", ["y0", "[0"]],
            [9, "default", "String", ["[0"]],
            [10, "const", "String", ["[0"]],
            [11, "attr", "Boolean", ["[0"]],
            [12, "nillable", "Boolean", ["[0"]],
            [13, "abstract", "Boolean", ["[0"]],
            [14, "extends", "TypeRef", ["[0"]],
            [15, "restricts", "TypeRef", ["[0"]],
            [16, "final", "Boolean", ["[0"]]
          ]],
          ["StringFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minInclusive", "String", ["[0"]],
            [3, "maxInclusive", "String", ["[0"]],
            [4, "minExclusive", "String", ["[0"]],
            [5, "maxExclusive", "String", ["[0"]],
            [6, "pattern", "String", ["/regex", "[0"]],
            [7, "minLength", "Integer", ["y0", "[0"]],
            [8, "maxLength", "Integer", ["y0", "[0"]],
            [9, "default", "String", ["[0"]],
            [10, "const", "String", ["[0"]],
            [11, "attr", "Boolean", ["[0"]],
            [12, "nillable", "Boolean", ["[0"]],
            [13, "abstract", "Boolean", ["[0"]],
            [14, "extends", "TypeRef", ["[0"]],
            [15, "restricts", "TypeRef", ["[0"]],
            [16, "final", "Boolean", ["[0"]],
            [17, "minOccurs", "Integer", ["y0", "[0"]],
            [18, "maxOccurs", "Integer", ["y-2", "[0"]],
            [19, "tagId", "Integer", ["[0"]],
            [20, "key", "Boolean", ["[0"]],
            [21, "link", "Boolean", ["[0"]],
            [22, "not", "Boolean", ["[0"]]
          ]],
          ["EnumeratedOpts", "Array", ["eAllOpts"], "", [
            [1, "id", "Boolean", ["[0"]],
            [2, "enum", "TypeRef", ["[0"]],
            [3, "pointer", "TypeRef", ["[0"]],
            [4, "attr", "Boolean", ["[0"]],
            [5, "nillable", "Boolean", ["[0"]],
            [6, "abstract", "Boolean", ["[0"]],
            [7, "extends", "TypeRef", ["[0"]],
            [8, "restricts", "TypeRef", ["[0"]],
            [9, "final", "Boolean", ["[0"]]
          ]],
          ["EnumeratedFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "id", "Boolean", ["[0"]],
            [2, "enum", "TypeRef", ["[0"]],
            [3, "pointer", "TypeRef", ["[0"]],
            [4, "attr", "Boolean", ["[0"]],
            [5, "nillable", "Boolean", ["[0"]],
            [6, "abstract", "Boolean", ["[0"]],
            [7, "extends", "TypeRef", ["[0"]],
            [8, "restricts", "TypeRef", ["[0"]],
            [9, "final", "Boolean", ["[0"]],
            [10, "minOccurs", "Integer", ["y0", "[0"]],
            [11, "maxOccurs", "Integer", ["y-2", "[0"]],
            [12, "tagId", "Integer", ["[0"]],
            [13, "key", "Boolean", ["[0"]],
            [14, "link", "Boolean", ["[0"]],
            [15, "not", "Boolean", ["[0"]]
          ]],
          ["ChoiceOpts", "Array", ["eAllOpts"], "", [
            [1, "id", "Boolean", ["[0"]],
            [2, "combine", "String", ["{1", "}1", "[0"]],
            [3, "nillable", "Boolean", ["[0"]],
            [4, "abstract", "Boolean", ["[0"]],
            [5, "extends", "TypeRef", ["[0"]],
            [6, "restricts", "TypeRef", ["[0"]],
            [7, "final", "Boolean", ["[0"]]
          ]],
          ["ChoiceFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "id", "Boolean", ["[0"]],
            [2, "combine", "String", ["{1", "}1", "[0"]],
            [3, "nillable", "Boolean", ["[0"]],
            [4, "abstract", "Boolean", ["[0"]],
            [5, "extends", "TypeRef", ["[0"]],
            [6, "restricts", "TypeRef", ["[0"]],
            [7, "final", "Boolean", ["[0"]],
            [8, "minOccurs", "Integer", ["y0", "[0"]],
            [9, "maxOccurs", "Integer", ["y-2", "[0"]],
            [10, "tagId", "Integer", ["[0"]],
            [11, "key", "Boolean", ["[0"]],
            [12, "link", "Boolean", ["[0"]],
            [13, "not", "Boolean", ["[0"]]
          ]],
          ["ArrayOpts", "Array", ["eAllOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minLength", "Integer", ["y0", "[0"]],
            [3, "maxLength", "Integer", ["y0", "[0"]],
            [4, "nillable", "Boolean", ["[0"]],
            [5, "abstract", "Boolean", ["[0"]],
            [6, "extends", "TypeRef", ["[0"]],
            [7, "restricts", "TypeRef", ["[0"]],
            [8, "final", "Boolean", ["[0"]]
          ]],
          ["ArrayFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minLength", "Integer", ["y0", "[0"]],
            [3, "maxLength", "Integer", ["y0", "[0"]],
            [4, "nillable", "Boolean", ["[0"]],
            [5, "abstract", "Boolean", ["[0"]],
            [6, "extends", "TypeRef", ["[0"]],
            [7, "restricts", "TypeRef", ["[0"]],
            [8, "final", "Boolean", ["[0"]],
            [9, "minOccurs", "Integer", ["y0", "[0"]],
            [10, "maxOccurs", "Integer", ["y-2", "[0"]],
            [11, "tagId", "Integer", ["[0"]],
            [12, "key", "Boolean", ["[0"]],
            [13, "link", "Boolean", ["[0"]],
            [14, "not", "Boolean", ["[0"]]
          ]],
          ["ArrayOfOpts", "Array", ["eAllOpts"], "", [
            [1, "vtype", "TypeRef"],
            [2, "minLength", "Integer", ["y0", "[0"]],
            [3, "maxLength", "Integer", ["y0", "[0"]],
            [4, "unique", "Boolean", ["[0"]],
            [5, "set", "Boolean", ["[0"]],
            [6, "unordered", "Boolean", ["[0"]],
            [7, "nillable", "Boolean", ["[0"]],
            [8, "abstract", "Boolean", ["[0"]],
            [9, "extends", "TypeRef", ["[0"]],
            [10, "restricts", "TypeRef", ["[0"]],
            [11, "final", "Boolean", ["[0"]]
          ]],
          ["ArrayOfFieldOpts", "Array", ["eAllOpts"], "", [
            [1, "vtype", "TypeRef"],
            [2, "minLength", "Integer", ["y0", "[0"]],
            [3, "maxLength", "Integer", ["y0", "[0"]],
            [4, "unique", "Boolean", ["[0"]],
            [5, "set", "Boolean", ["[0"]],
            [6, "unordered", "Boolean", ["[0"]],
            [7, "nillable", "Boolean", ["[0"]],
            [8, "abstract", "Boolean", ["[0"]],
            [9, "extends", "TypeRef", ["[0"]],
            [10, "restricts", "TypeRef", ["[0"]],
            [11, "final", "Boolean", ["[0"]],
            [12, "minOccurs", "Integer", ["y0", "[0"]],
            [13, "maxOccurs", "Integer", ["y-2", "[0"]],
            [14, "tagId", "Integer", ["[0"]],
            [15, "key", "Boolean", ["[0"]],
            [16, "link", "Boolean", ["[0"]],
            [17, "not", "Boolean", ["[0"]]
          ]],
          ["MapOpts", "Array", ["eAllOpts"], "", [
            [1, "id", "Boolean", ["[0"]],
            [2, "minLength", "Integer", ["y0", "[0"]],
            [3, "maxLength", "Integer", ["y0", "[0"]],
            [4, "sequence", "Boolean", ["[0"]],
            [5, "nillable", "Boolean", ["[0"]],
            [6, "abstract", "Boolean", ["[0"]],
            [7, "extends", "TypeRef", ["[0"]],
            [8, "restricts", "TypeRef", ["[0"]],
            [9, "final", "Boolean", ["[0"]]
          ]],
          ["MapFieldOpts", "Array", ["eAllOpts"], "", [
            [1, "id", "Boolean", ["[0"]],
            [2, "minLength", "Integer", ["y0", "[0"]],
            [3, "maxLength", "Integer", ["y0", "[0"]],
            [4, "sequence", "Boolean", ["[0"]],
            [5, "nillable", "Boolean", ["[0"]],
            [6, "abstract", "Boolean", ["[0"]],
            [7, "extends", "TypeRef", ["[0"]],
            [8, "restricts", "TypeRef", ["[0"]],
            [9, "final", "Boolean", ["[0"]],
            [10, "minOccurs", "Integer", ["y0", "[0"]],
            [11, "maxOccurs", "Integer", ["y-2", "[0"]],
            [12, "tagId", "Integer", ["[0"]],
            [13, "key", "Boolean", ["[0"]],
            [14, "link", "Boolean", ["[0"]],
            [15, "not", "Boolean", ["[0"]]
          ]],
          ["MapOfOpts", "Array", ["eAllOpts"], "", [
            [1, "ktype", "TypeRef"],
            [2, "vtype", "TypeRef"],
            [3, "minLength", "Integer", ["y0", "[0"]],
            [4, "maxLength", "Integer", ["y0", "[0"]],
            [5, "sequence", "Boolean", ["[0"]],
            [6, "nillable", "Boolean", ["[0"]],
            [7, "abstract", "Boolean", ["[0"]],
            [8, "extends", "TypeRef", ["[0"]],
            [9, "restricts", "TypeRef", ["[0"]],
            [10, "final", "Boolean", ["[0"]]
          ]],
          ["MapOfFieldOpts", "Array", ["eAllOpts"], "", [
            [1, "ktype", "TypeRef"],
            [2, "vtype", "TypeRef"],
            [3, "minLength", "Integer", ["y0", "[0"]],
            [4, "maxLength", "Integer", ["y0", "[0"]],
            [5, "sequence", "Boolean", ["[0"]],
            [6, "nillable", "Boolean", ["[0"]],
            [7, "abstract", "Boolean", ["[0"]],
            [8, "extends", "TypeRef", ["[0"]],
            [9, "restricts", "TypeRef", ["[0"]],
            [10, "final", "Boolean", ["[0"]],
            [11, "minOccurs", "Integer", ["y0", "[0"]],
            [12, "maxOccurs", "Integer", ["y-2", "[0"]],
            [13, "tagId", "Integer", ["[0"]],
            [14, "key", "Boolean", ["[0"]],
            [15, "link", "Boolean", ["[0"]],
            [16, "not", "Boolean", ["[0"]]
          ]],
          ["RecordOpts", "Array", ["eAllOpts"], "", [
            [1, "minLength", "Integer", ["y0", "[0"]],
            [2, "maxLength", "Integer", ["y0", "[0"]],
            [3, "sequence", "Boolean", ["[0"]],
            [4, "nillable", "Boolean", ["[0"]],
            [5, "abstract", "Boolean", ["[0"]],
            [6, "extends", "TypeRef", ["[0"]],
            [7, "restricts", "TypeRef", ["[0"]],
            [8, "final", "Boolean", ["[0"]]
          ]],
          ["RecordFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "minLength", "Integer", ["y0", "[0"]],
            [2, "maxLength", "Integer", ["y0", "[0"]],
            [3, "sequence", "Boolean", ["[0"]],
            [4, "nillable", "Boolean", ["[0"]],
            [5, "abstract", "Boolean", ["[0"]],
            [6, "extends", "TypeRef", ["[0"]],
            [7, "restricts", "TypeRef", ["[0"]],
            [8, "final", "Boolean", ["[0"]],
            [9, "minOccurs", "Integer", ["y0", "[0"]],
            [10, "maxOccurs", "Integer", ["y-2", "[0"]],
            [11, "tagId", "Integer", ["[0"]],
            [12, "key", "Boolean", ["[0"]],
            [13, "link", "Boolean", ["[0"]],
            [14, "not", "Boolean", ["[0"]]
          ]]
        ]
      }
    


    valid_data_list = [            
            
            ["Schema", "Record", [], "", [
                [1, "meta", "String", [], ""],
                [2, "types", "String", ["[1", "]-1"], ""]]]
        ]}
      
    valid_data_list = [
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "String", ["[0"], "", []]]        
        }, 
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Binary", [], ""]]        
        },               
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Integer", ["[0"], "", []]]        
        },          
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Number", ["[0"], "", []]]        
        },    
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Enumerated", [], "", [
                [1, "thing", ""],
                [2, "two", ""]]

            ]]        
        }, 
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Array", [], "", [
                [1, "thing", "String", [], ""]]

            ]]        
        },      
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Record", [], "", [
                [1, "thing", "String", [], ""]]
            ]]        
        },      
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Map", [], "", [
                [1, "thing", "String", [], ""]]

            ]]        
        },      
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "ArrayOf", ["*String"], ""

            ]]        
        },      
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "MapOf", ["+Integer", "*String"], ""

            ]]        
        },

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
            "meta" : "package",
            "types" : ["Typename2"]       
        }]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
    
def test_types_validity(): 
    root = "Type"    
  
    j_schema = {
    "meta": {
      "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
      "roots": ["Types-Map"],
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
"""

{
  "meta": {
    "title": "Music Library",
    "package": "http://fake-audio.org/music-lib",
    "version": "1.1",
    "description": "This information model defines a library of audio tracks, organized by album, with associated metadata regarding each track. It is modeled on the types of library data maintained by common websites and music file tag editors.",
    "license": "CC0-1.0",
    "roots": ["Library"]
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

def test_ui_issue_08282025():
  data = {
    "meta": {
      "package": "http://test/v1.0",
      "roots": ["Record-Name"]
    },
    "types": [
      ["Record-Name", "Record", [], "", [
          [1, "field_value_1", "String", [], ""]
        ]]
    ]
  }
  
  j_meta_schema = {
        "meta": {
        "title": "JADN Metaschema",
        "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
        "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
        "license": "CC-BY-4.0",
        "roots": ["Schema"],
            "config": {
                "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$"
            }
        },

        "types": [
        ["Schema", "Record", [], "Definition of a JADN package", [
            [1, "meta", "Metadata", ["[0"], "Information about this package"],
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
            [9, "roots", "TypeName", ["[0", "]-1"], "Roots of the type tree(s) in this package"],
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
            [2, "core_type", "Enumerated", ["#JADN-Type"], ""],
            [3, "type_options", "Options", ["[0"], ""],
            [4, "type_description", "Description", ["[0"], ""],
            [5, "fields", "JADN-Type", ["[0", "&2"], ""]
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

        ["Items", "ArrayOf", ["*Item"], ""],

        ["Fields", "ArrayOf", ["*Field"], ""],

        ["Item", "Array", [], "", [
            [1, "item_id", "FieldID", [], ""],
            [2, "item_value", "String", [], ""],
            [3, "item_description", "Description", ["[0"], ""]
        ]],

        ["Field", "Array", [], "", [
            [1, "field_id", "FieldID", [], ""],
            [2, "field_name", "FieldName", [], ""],
            [3, "field_type", "TypeRef", [], ""],
            [4, "field_options", "Options", ["[0"], ""],
            [5, "field_description", "Description", ["[0"], ""]
        ]],

        ["FieldID", "Integer", ["y0"], ""],

        ["Options", "ArrayOf", ["*Option"], ""],

        ["Option", "String", ["{1"], ""],

        ["Description", "String", [], ""]
        ]
    } 
    
    
  passed = False  
  try :
      j_validation = DataValidation(j_meta_schema, "Schema", data)
      j_validation.validate()
      passed = True
  except Exception as e:
      print(e)
    
  assert passed
  
def test_ui_issue_09022025():
  data = {
    # "Binary-Fmt": {
      "lower_x": "acbd",
      "upper_x": "ABCD",
      "base64": "ABCD"
    # }
  }
  
  j_meta_schema = {
    "meta": {
      "package": "https://www.test.com/",
      # "roots": ["Decimal-Integer", "Binary-Fmt"]
      "roots": ["Binary-Fmt"]
    },
    "types": [
      # ["Decimal-Integer", "Record", [], "", [
      #     [1, "i64", "Integer", ["/i64"], ""],
      #     [2, "non_negative_integer", "Integer", ["/nonNegativeInteger"], ""],
      #     [3, "negative_integer", "Integer", ["/negativeInteger"], ""],
      #     [4, "non_positive_integer", "Integer", ["/nonPositiveInteger"], ""],
      #     [5, "positive_integer", "Integer", ["/positiveInteger"], ""],
      #     [6, "unsigned_short", "Integer", ["/u16"], ""]
      #   ]],
      ["Binary-Fmt", "Record", [], "", [
          [1, "lower_x", "Binary", ["/x", "[0"], ""],
          [2, "upper_x", "Binary", ["/X", "[0"], ""],
          [3, "base64", "Binary", ["/b64", "[0"], ""]
        ]]
    ]
  }
    
    
  passed = False  
  try :
      j_validation = DataValidation(j_meta_schema, "Binary-Fmt", data)
      j_validation.validate()
      passed = True
  except Exception as e:
      print(e)
    
  assert passed  

def test_ui_issue_09032025():
  data = {
    "i64_value_1": 92233720368547760,
    "i32_value_2": 2147483647,
    "i16_value_3": 32767,
    "i8_value_4": 127,
    "nonneg_value_5": 0,
    "posint_value_6": 1,
    "u64_value_7": 18446744073709551615,
    "u32_value_8": 4294967294,
    "u16_value_9": 32767,
    "u8_value_10": 127,
    "nonpos_value_11": 0,
    "negint_value_12": -1
  }

  j_meta_schema = {
    "meta": {
      "title": "JADN Schema Start Up Template",
      "package": "http://JADN-Schema-Start-Up-Template-URI",
      "roots": ["Schema"]
    },
    "types": [
      ["Schema", "Record", [], "", [
          [1, "i64_value_1", "Integer", ["/i64"], ""],
          [2, "i32_value_2", "Integer", ["/i32"], ""],
          [3, "i16_value_3", "Integer", ["/i16"], ""],
          [4, "i8_value_4", "Integer", ["/i8"], ""],
          [5, "nonneg_value_5", "Integer", ["/nonNegativeInteger"], ""],
          [6, "posint_value_6", "Integer", ["/positiveInteger"], ""],
          [7, "u64_value_7", "Integer", ["/u64"], ""],
          [8, "u32_value_8", "Integer", ["/u32"], ""],
          [9, "u16_value_9", "Integer", ["/u16"], ""],
          [10, "u8_value_10", "Integer", ["/u8"], ""],
          [11, "nonpos_value_11", "Integer", ["/nonPositiveInteger"], ""],
          [12, "negint_value_12", "Integer", ["/negativeInteger"], ""]
        ]]
    ]
  }

  passed = False  
  try :
      j_validation = DataValidation(j_meta_schema, "Schema", data)
      j_validation.validate()
      passed = True
  except Exception as e:
      print(e)

def test_ui_issue_09032025_2():
  data = {
    "normalized_string": "letter",
    "token": "Milwaukee",
    "language": "en-US",
    "name": "_name",
    "any_uri": "http://www.test.com",
    "qname": "www.example.com:Homepage"
  }

  j_meta_schema = {
    "meta": {
      "package": "https://www.test.com",
      "roots": ["Decimal-Integer", "Binary-Fmt", "Integer-Fmts", "String-Fmts"]
    },
    "types": [
      ["Decimal-Integer", "Record", [], "", [
          [1, "u64", "Integer", ["/u64"], ""],
          [2, "i64", "Integer", ["/i64"], ""],
          [3, "non_negative_integer", "Integer", ["/nonNegativeInteger"], ""],
          [4, "negative_integer", "Integer", ["/negativeInteger"], ""],
          [5, "non_positive_integer", "Integer", ["/nonPositiveInteger"], ""],
          [6, "positive_integer", "Integer", ["/positiveInteger"], ""],
          [7, "unsigned_short", "Integer", ["/u16"], ""]
        ]],
      ["Binary-Fmt", "Record", [], "", [
          [1, "lower_x", "Binary", ["/x", "[0"], ""],
          [2, "upper_x", "Binary", ["/X", "[0"], ""],
          [3, "base64", "Binary", ["/b64", "[0"], ""]
        ]],
      ["Integer-Fmts", "Record", [], "", [
          [1, "int_date_time", "Integer", ["/date-time"], ""],
          [2, "string_date_time", "String", ["/date-time"], ""],
          [3, "int_date", "Integer", ["/date"], ""],
          [4, "string_date", "String", ["/date"], ""],
          [5, "time", "Integer", ["/time"], ""],
          [6, "string_time", "String", ["/time"], ""],
          [7, "g_year_month", "Integer", ["/gYearMonth"], ""],
          [8, "g_year", "Integer", ["/gYear"], ""],
          [9, "g_month_day", "Integer", ["/gMonthDay"], ""],
          [10, "duration_test", "Integer", ["/duration"], ""],
          [11, "day_time_duration", "Integer", ["/dayTimeDuration"], ""],
          [12, "year_month_duration", "Integer", ["/yearMonthDuration"], ""]
        ]],
      ["String-Fmts", "Record", [], "", [
          [1, "normalized_string", "String", ["/normalizedString"], ""],
          [2, "token", "String", ["/token"], ""],
          [3, "language", "String", ["/language"], ""],
          [4, "name", "String", ["/name"], ""],
          [5, "any_uri", "String", ["/anyUri"], ""],
          [6, "qname", "String", ["/QName"], ""]
        ]]
    ]
  }

  passed = False  
  try :
      j_validation = DataValidation(j_meta_schema, "String-Fmts", data)
      j_validation.validate()
      passed = True
  except Exception as e:
      print(e)

def test_config_fields(): 
    root = "Metadata"    
  
    j_schema = {
    "meta": {
      "title": "JADN Metaschema",
      "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
      "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
      "license": "CC-BY-4.0",
      "roots": ["Metadata"],
      "config": {
        "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$",
      }
    },

    "types": [
      ["Schema", "Record", [], "Definition of a JADN package", [
        [1, "meta", "Metadata", ["[0"], "Information about this package"],
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
        [9, "roots", "TypeName", ["[0", "]-1"], "Roots of the type tree(s) in this package"],
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
    "roots": ["Record-Name"],
    "config": {
        "$MaxBinary": 255,
        "$MaxString": 5555,
        "$MaxElements": 555,
        "$Sys": "$",
        "$TypeName": "^[A-Za-z][-_$A-Za-z0-9]{0,63}$",
        "$FieldName": "^[A-Za-z][-_A-Za-z0-9]{0,63}$",
        "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
    }
  }

    
    
    valid_data_list = [ valid_data ]
    invalid_data_list = [

         {'SuitEnum': 10},'Aces', 10
         
         ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_ui_issue_09042025(): #OSCAL POAM
    root = "Metadata"    
  
    j_schema = {
    "meta": {
      "title": "JADN Metaschema",
      "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
      "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
      "license": "CC-BY-4.0",
      "roots": ["Metadata"],
      "config": {
        "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$",
      }
    },

    "types": [
      ["Schema", "Record", [], "Definition of a JADN package", [
        [1, "meta", "Metadata", ["[0"], "Information about this package"],
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
        [9, "roots", "TypeName", ["[0", "]-1"], "Roots of the type tree(s) in this package"],
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
      "meta": {
        "package": "http://csrc.nist.gov/ns/oscal/1.1.1/oscal-poam-schema.json",
        "comment": "OSCAL Plan of Action and Milestones (POA&M) Model: JSON Schema",
        "roots": ["Root"],
        "config": {
            "$MaxBinary": 255,
            "$MaxString": 5555,
            "$MaxElements": 555,
            "$Sys": "$",
            "$TypeName": "^[A-Za-z][-_$A-Za-z0-9]{0,63}$",
            "$FieldName": "^[A-Za-z][-_A-Za-z0-9]{0,63}$",
            "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
        }
      },

      "types": [
        ["Root", "Record", [], "", [
          [1, "schema", "URIReferenceDatatype", ["[0"], "A JSON Schema directive to bind a specific schema to its document instance."],
          [2, "plan-of-action-and-milestones", "Plan-of-action-and-milestones", [], "A plan of action and milestones which identifies initial and residual risks, deviations, and disposition, such as those required by FedRAMP."]
        ]],

        ["Plan-of-action-and-milestones", "Record", [], "A plan of action and milestones which identifies initial and residual risks, deviations, and disposition, such as those required by FedRAMP.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with instancescope that can be used to reference this POA&M instance in this OSCAL instance. This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "metadata", "Metadata", [], "Provides information about the containing document, and defines concepts that are shared across the document."],
          [3, "import-ssp", "Import-ssp", ["[0"], "Used by the assessment plan and POA&M to import information about the system."],
          [4, "system-id", "System-id", ["[0"], "A human-oriented, globally unique identifier with cross-instance scope that can be used to reference this system identification property elsewhere in this or other OSCAL instances. When referencing an externally defined system identification, the system identification must be used in the context of the external / imported OSCAL instance (e.g., uri-reference). This string should be assigned per-subject, which means it should be consistently used to identify the same system across revisions of the document."],
          [5, "local-definitions", "Local-definitions", ["[0"], "Allows components, and inventory-items to be defined within the POA&M for circumstances where no OSCAL-based SSP exists, or is not delivered with the POA&M."],
          [6, "observations", "Observations", ["[0"], "Describes an individual observation."],
          [7, "risks", "Risks", ["[0"], "An identified risk."],
          [8, "findings", "Findings", ["[0"], "Describes an individual finding."],
          [9, "poam-items", "Poam-items", [], "Describes an individual POA&M item."],
          [10, "back-matter", "Back-matter", ["[0"], "A collection of resources that may be referenced from within the OSCAL document instance."]
        ]],

        ["Observations", "ArrayOf", ["{1", "*Observation"], "", []],

        ["Risks", "ArrayOf", ["{1", "*Risk"], "", []],

        ["Findings", "ArrayOf", ["{1", "*Finding"], "", []],

        ["Poam-items", "ArrayOf", ["{1", "*Poam-item"], "", []],

        ["Local-definitions", "Record", [], "Allows components, and inventory-items to be defined within the POA&M for circumstances where no OSCAL-based SSP exists, or is not delivered with the POA&M.", [
          [1, "components", "Components", ["[0"], "A defined component that can be part of an implemented system."],
          [2, "inventory-items", "Inventory-items", ["[0"], "A single managed inventory item within the system."],
          [3, "assessment-assets", "Assessment-assets", ["[0"], "Identifies the assets used to perform this assessment, such as the assessment team, scanning tools, and assumptions."],
          [4, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Components", "ArrayOf", ["{1", "*System-component"], "", []],

        ["Inventory-items", "ArrayOf", ["{1", "*Inventory-item"], "", []],

        ["Poam-item", "Record", [], "Describes an individual POA&M item.", [
          [1, "uuid", "UUIDDatatype", ["[0"], "A machine-oriented, globally unique identifier with instance scope that can be used to reference this POA&M item entry in this OSCAL instance. This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "title", "String", [], "The title or name for this POA&M item ."],
          [3, "description", "String", [], "A human-readable description of POA&M item."],
          [4, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [5, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [6, "origins", "Actors", ["[0"], "Identifies the source of the finding, such as a tool or person."],
          [7, "related-findings", "Related-findings", ["[0"], "Relates the poam-item to referenced finding(s)."],
          [8, "related-observations", "Related-observations", ["[0"], "Relates the poam-item to a set of referenced observations that were used to determine the finding."],
          [9, "related-risks", "Related-risks", ["[0"], "Relates the finding to a set of referenced risks that were used to determine the finding."],
          [10, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Props", "ArrayOf", ["{1", "*Property"], "", []],

        ["Links", "ArrayOf", ["{1", "*Link"], "", []],

        ["Origins", "ArrayOf", ["{1", "*Origin"], "", []],

        ["Actors", "ArrayOf", ["{1", "*Origin-actor"], "", []],

        ["Related-findings", "ArrayOf", ["{1", "*Related-finding"], "", []],

        ["Related-finding", "Record", [], "Relates the poam-item to referenced finding(s).", [
          [1, "finding-uuid", "UUIDDatatype", [], "A machine-oriented identifier reference to a finding defined in the list of findings."]
        ]],

        ["Related-observations", "ArrayOf", ["{1", "*Related-observation"], "", []],

        ["Related-observation", "Record", [], "Relates the poam-item to a set of referenced observations that were used to determine the finding.", [
          [1, "observation-uuid", "UUIDDatatype", [], "A machine-oriented identifier reference to an observation defined in the list of observations."]
        ]],

        ["Related-risks", "ArrayOf", ["{1", "*Related-risk"], "", []],

        ["Related-risk", "Record", [], "Relates the finding to a set of referenced risks that were used to determine the finding.", [
          [1, "risk-uuid", "UUIDDatatype", [], "A machine-oriented identifier reference to a risk defined in the list of risks."]
        ]],

        ["Metadata", "Record", [], "Provides information about the containing document, and defines concepts that are shared across the document.", [
          [1, "title", "String", [], "A name given to the document, which may be used by a tool for display and navigation."],
          [2, "published", "DateTimeWithTimezoneDatatype", ["[0"], "The date and time the document was last made available."],
          [3, "last-modified", "DateTimeWithTimezoneDatatype", [], "The date and time the document was last stored for later retrieval."],
          [4, "version", "StringDatatype", [], "Used to distinguish a specific revision of an OSCAL document from other previous and future versions."],
          [5, "oscal-version", "StringDatatype", [], "The OSCAL model version the document was authored against and will conform to as valid."],
          [6, "revisions", "Revisions", ["[0"], "An entry in a sequential list of revisions to the containing document, expected to be in reverse chronological order (i.e. latest first)."],
          [7, "document-ids", "Document-ids", ["[0"], "A document identifier qualified by an identifier scheme."],
          [8, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [9, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [10, "roles", "Roles", ["[0"], "Defines a function, which might be assigned to a party in a specific situation."],
          [11, "locations", "Locations", ["[0"], "A physical point of presence, which may be associated with people, organizations, or other concepts within the current or linked OSCAL document."],
          [12, "parties", "Parties", ["[0"], "An organization or person, which may be associated with roles or other concepts within the current or linked OSCAL document."],
          [13, "responsible-parties", "Responsible-parties", ["[0"], "A reference to a set of persons and/or organizations that have responsibility for performing the referenced role in the context of the containing object."],
          [14, "actions", "Actions", ["[0"], "An action applied by a role within a given party to the content."],
          [15, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Revisions", "ArrayOf", ["{1", "*Revision"], "", []],

        ["Revision", "Record", [], "An entry in a sequential list of revisions to the containing document, expected to be in reverse chronological order (i.e. latest first).", [
          [1, "title", "String", ["[0"], "A name given to the document revision, which may be used by a tool for display and navigation."],
          [2, "published", "DateTimeWithTimezoneDatatype", ["[0"], "The date and time the document was last made available."],
          [3, "last-modified", "DateTimeWithTimezoneDatatype", ["[0"], "The date and time the document was last stored for later retrieval."],
          [4, "version", "StringDatatype", [], "Used to distinguish a specific revision of an OSCAL document from other previous and future versions."],
          [5, "oscal-version", "StringDatatype", ["[0"], "The OSCAL model version the document was authored against and will conform to as valid."],
          [6, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [7, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [8, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Document-ids", "ArrayOf", ["{1", "*Document-id"], "", []],

        ["Roles", "ArrayOf", ["{1", "*Role"], "", []],

        ["Role", "Record", [], "Defines a function, which might be assigned to a party in a specific situation.", [
          [1, "id", "TokenDatatype", [], "A unique identifier for the role."],
          [2, "title", "String", [], "A name given to the role, which may be used by a tool for display and navigation."],
          [3, "short-name", "StringDatatype", ["[0"], "A short common name, abbreviation, or acronym for the role."],
          [4, "description", "String", ["[0"], "A summary of the role's purpose and associated responsibilities."],
          [5, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [6, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [7, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Locations", "ArrayOf", ["{1", "*Location"], "", []],

        ["Location", "Record", [], "A physical point of presence, which may be associated with people, organizations, or other concepts within the current or linked OSCAL document.", [
          [1, "uuid", "UUIDDatatype", [], "A unique ID for the location, for reference."],
          [2, "title", "String", ["[0"], "A name given to the location, which may be used by a tool for display and navigation."],
          [3, "address", "Address", ["[0"], "A postal address for the location."],
          [4, "email-addresses", "Email-addresses", ["[0"], "An email address as defined by RFC 5322 Section 3.4.1."],
          [5, "telephone-numbers", "Telephone-numbers", ["[0"], "A telephone service number as defined by ITU-T E.164."],
          [6, "urls", "Urls", ["[0"], "The uniform resource locator (URL) for a web site or other resource associated with the location."],
          [7, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [8, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [9, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Email-addresses", "ArrayOf", ["{1", "*EmailAddressDatatype"], "", []],

        ["Telephone-numbers", "ArrayOf", ["{1", "*Telephone-number"], "", []],

        ["Urls", "ArrayOf", ["{1", "*URIDatatype"], "", []],

        ["Parties", "ArrayOf", ["{1", "*Party"], "", []],

        ["Party", "Record", [], "An organization or person, which may be associated with roles or other concepts within the current or linked OSCAL document.", [
          [1, "uuid", "UUIDDatatype", [], "A unique identifier for the party."],
          [2, "type", "Party$type", [], "A category describing the kind of party the object describes."],
          [3, "name", "StringDatatype", ["[0"], "The full name of the party. This is typically the legal name associated with the party."],
          [4, "short-name", "StringDatatype", ["[0"], "A short common name, abbreviation, or acronym for the party."],
          [5, "external-ids", "External-ids", ["[0"], "An identifier for a person or organization using a designated scheme. e.g. an Open Researcher and Contributor ID (ORCID)."],
          [6, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [7, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [8, "email-addresses", "Email-addresses", ["[0"], "An email address as defined by RFC 5322 Section 3.4.1."],
          [9, "telephone-numbers", "Telephone-numbers", ["[0"], "A telephone service number as defined by ITU-T E.164."],
          [10, "addresses", "Addresses", ["[0"], "A postal address for the location."],
          [11, "location-uuids", "Location-uuids", ["[0"], "Reference to a location by UUID."],
          [12, "member-of-organizations", "Member-of-organizations", ["[0"], "A reference to another party by UUID, typically an organization, that this subject is associated with."],
          [13, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Party$type", "Choice", [], "A category describing the kind of party the object describes.", [
          [1, "c1", "StringDatatype", [], ""],
          [2, "c2", "Party$type$2", [], ""]
        ]],

        ["Party$type$2", "Enumerated", [], "", [
          [1, "person", ""],
          [2, "organization", ""]
        ]],

        ["External-ids", "ArrayOf", ["{1", "*External-id"], "", []],

        ["External-id", "Record", [], "An identifier for a person or organization using a designated scheme. e.g. an Open Researcher and Contributor ID (ORCID).", [
          [1, "scheme", "External-id$scheme", [], "Indicates the type of external identifier."],
          [2, "id", "StringDatatype", [], ""]
        ]],

        ["External-id$scheme", "Choice", [], "Indicates the type of external identifier.", [
          [1, "c1", "URIDatatype", [], ""],
          [2, "c2", "External-id$scheme$2", [], ""]
        ]],

        ["External-id$scheme$2", "Enumerated", [], "", [
          [1, "http://orcid.org/", ""]
        ]],

        ["Addresses", "ArrayOf", ["{1", "*Address"], "", []],

        ["Location-uuids", "ArrayOf", ["{1", "*UUIDDatatype"], "", []],

        ["Member-of-organizations", "ArrayOf", ["{1", "*UUIDDatatype"], "", []],

        ["Responsible-parties", "ArrayOf", ["{1", "*Responsible-party"], "", []],

        ["Actions", "ArrayOf", ["{1", "*Action"], "", []],

        ["Back-matter", "Record", [], "A collection of resources that may be referenced from within the OSCAL document instance.", [
          [1, "resources", "Resources", ["[0"], "A resource associated with content in the containing document instance. A resource may be directly included in the document using base64 encoding or may point to one or more equivalent internet resources."]
        ]],

        ["Resources", "ArrayOf", ["{1", "*Resource"], "", []],

        ["Resource", "Record", [], "A resource associated with content in the containing document instance. A resource may be directly included in the document using base64 encoding or may point to one or more equivalent internet resources.", [
          [1, "uuid", "UUIDDatatype", [], "A unique identifier for a resource."],
          [2, "title", "String", ["[0"], "An optional name given to the resource, which may be used by a tool for display and navigation."],
          [3, "description", "String", ["[0"], "An optional short summary of the resource used to indicate the purpose of the resource."],
          [4, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [5, "document-ids", "Document-ids", ["[0"], "A document identifier qualified by an identifier scheme."],
          [6, "citation", "Resource", ["[0"], "An optional citation consisting of end note text using structured markup."],
          [7, "rlinks", "Rlinks", ["[0"], "A URL-based pointer to an external resource with an optional hash for verification and change detection."],
          [8, "base64", "Resource", ["[0"], "A resource encoded using the Base64 alphabet defined by RFC 2045."],
          [9, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Rlinks", "ArrayOf", ["{1", "*Rlink"], "", []],

        ["Rlink", "Record", [], "A URL-based pointer to an external resource with an optional hash for verification and change detection.", [
          [1, "href", "URIReferenceDatatype", [], "A resolvable URL pointing to the referenced resource."],
          [2, "media-type", "StringDatatype", ["[0"], "A label that indicates the nature of a resource, as a data serialization or format."],
          [3, "hashes", "Hashes", ["[0"], "A representation of a cryptographic digest generated over a resource using a specified hash algorithm."]
        ]],

        ["Hashes", "ArrayOf", ["{1", "*Hash"], "", []],

        ["Property", "Record", [], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair.", [
          [1, "name", "TokenDatatype", [], "A textual label, within a namespace, that uniquely identifies a specific attribute, characteristic, or quality of the property's containing object."],
          [2, "uuid", "UUIDDatatype", ["[0"], "A unique identifier for a property."],
          [3, "ns", "URIDatatype", ["[0"], "A namespace qualifying the property's name. This allows different organizations to associate distinct semantics with the same name."],
          [4, "value", "StringDatatype", [], "Indicates the value of the attribute, characteristic, or quality."],
          [5, "class", "TokenDatatype", ["[0"], "A textual label that provides a sub-type or characterization of the property's name."],
          [6, "group", "TokenDatatype", ["[0"], "An identifier for relating distinct sets of properties."],
          [7, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Link", "Record", [], "A reference to a local or remote resource, that has a specific relation to the containing object.", [
          [1, "href", "URIReferenceDatatype", [], "A resolvable URL reference to a resource."],
          [2, "rel", "Link$rel", ["[0"], "Describes the type of relationship provided by the link's hypertext reference. This can be an indicator of the link's purpose."],
          [3, "media-type", "StringDatatype", ["[0"], "A label that indicates the nature of a resource, as a data serialization or format."],
          [4, "resource-fragment", "StringDatatype", ["[0"], "In case where the href points to a back-matter/resource, this value will indicate the URI fragment to append to any rlink associated with the resource. This value MUST be URI encoded."],
          [5, "text", "String", ["[0"], "A textual label to associate with the link, which may be used for presentation in a tool."]
        ]],

        ["Link$rel", "Choice", [], "Describes the type of relationship provided by the link's hypertext reference. This can be an indicator of the link's purpose.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Link$rel$2", [], ""]
        ]],

        ["Link$rel$2", "Enumerated", [], "", [
          [1, "reference", ""]
        ]],

        ["Responsible-party", "Record", [], "A reference to a set of persons and/or organizations that have responsibility for performing the referenced role in the context of the containing object.", [
          [1, "role-id", "TokenDatatype", [], "A reference to a role performed by a party."],
          [2, "party-uuids", "Party-uuids", [], "Reference to a party by UUID."],
          [3, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [4, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [5, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Party-uuids", "ArrayOf", ["{1", "*UUIDDatatype"], "", []],

        ["Action", "Record", [], "An action applied by a role within a given party to the content.", [
          [1, "uuid", "UUIDDatatype", [], "A unique identifier that can be used to reference this defined action elsewhere in an OSCAL document. A UUID should be consistently used for a given location across revisions of the document."],
          [2, "date", "DateTimeWithTimezoneDatatype", ["[0"], "The date and time when the action occurred."],
          [3, "type", "TokenDatatype", [], "The type of action documented by the assembly, such as an approval."],
          [4, "system", "URIDatatype", [], "Specifies the action type system used."],
          [5, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [6, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [7, "responsible-parties", "Responsible-parties", ["[0"], "A reference to a set of persons and/or organizations that have responsibility for performing the referenced role in the context of the containing object."],
          [8, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Responsible-role", "Record", [], "A reference to a role with responsibility for performing a function relative to the containing object, optionally associated with a set of persons and/or organizations that perform that role.", [
          [1, "role-id", "TokenDatatype", [], "A human-oriented identifier reference to a role performed."],
          [2, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [3, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [4, "party-uuids", "Party-uuids", ["[0"], "Reference to a party by UUID."],
          [5, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Hash", "Record", [], "A representation of a cryptographic digest generated over a resource using a specified hash algorithm.", [
          [1, "algorithm", "Hash$algorithm", [], "The digest method by which a hash is derived."],
          [2, "value", "StringDatatype", [], ""]
        ]],

        ["Hash$algorithm", "Choice", [], "The digest method by which a hash is derived.", [
          [1, "c1", "StringDatatype", [], ""],
          [2, "c2", "Hash$algorithm$2", [], ""]
        ]],

        ["Hash$algorithm$2", "Enumerated", [], "", [
          [1, "SHA-224", ""],
          [2, "SHA-256", ""],
          [3, "SHA-384", ""],
          [4, "SHA-512", ""],
          [5, "SHA3-224", ""],
          [6, "SHA3-256", ""],
          [7, "SHA3-384", ""],
          [8, "SHA3-512", ""]
        ]],

        ["Remarks", "String", [], "Additional commentary about the containing object.", []],

        ["Telephone-number", "Record", [], "A telephone service number as defined by ITU-T E.164.", [
          [1, "type", "Telephone-number$type", ["[0"], "Indicates the type of phone number."],
          [2, "number", "StringDatatype", [], ""]
        ]],

        ["Telephone-number$type", "Choice", [], "Indicates the type of phone number.", [
          [1, "c1", "StringDatatype", [], ""],
          [2, "c2", "Telephone-number$type$2", [], ""]
        ]],

        ["Telephone-number$type$2", "Enumerated", [], "", [
          [1, "home", ""],
          [2, "office", ""],
          [3, "mobile", ""]
        ]],

        ["Address", "Record", [], "A postal address for the location.", [
          [1, "type", "Address$type", ["[0"], "Indicates the type of address."],
          [2, "addr-lines", "Addr-lines", ["[0"], "A single line of an address."],
          [3, "city", "StringDatatype", ["[0"], "City, town or geographical region for the mailing address."],
          [4, "state", "StringDatatype", ["[0"], "State, province or analogous geographical region for a mailing address."],
          [5, "postal-code", "StringDatatype", ["[0"], "Postal or ZIP code for mailing address."],
          [6, "country", "StringDatatype", ["[0"], "The ISO 3166-1 alpha-2 country code for the mailing address."]
        ]],

        ["Address$type", "Choice", [], "Indicates the type of address.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Address$type$2", [], ""]
        ]],

        ["Address$type$2", "Enumerated", [], "", [
          [1, "home", ""],
          [2, "work", ""]
        ]],

        ["Addr-lines", "ArrayOf", ["{1", "*StringDatatype"], "", []],

        ["Document-id", "Record", [], "A document identifier qualified by an identifier scheme.", [
          [1, "scheme", "Document-id$scheme", ["[0"], "Qualifies the kind of document identifier using a URI. If the scheme is not provided the value of the element will be interpreted as a string of characters."],
          [2, "identifier", "StringDatatype", [], ""]
        ]],

        ["Document-id$scheme", "Choice", [], "Qualifies the kind of document identifier using a URI. If the scheme is not provided the value of the element will be interpreted as a string of characters.", [
          [1, "c1", "URIDatatype", [], ""],
          [2, "c2", "Document-id$scheme$2", [], ""]
        ]],

        ["Document-id$scheme$2", "Enumerated", [], "", [
          [1, "http://www.doi.org/", ""]
        ]],

        ["System-component", "Record", [], "A defined component that can be part of an implemented system.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this component elsewhere in this or other OSCAL instances. The locally defined UUID of the component can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "type", "System-component$type", [], "A category describing the purpose of the component."],
          [3, "title", "String", [], "A human readable name for the system component."],
          [4, "description", "String", [], "A description of the component, including information about its function."],
          [5, "purpose", "String", ["[0"], "A summary of the technological or business purpose of the component."],
          [6, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [7, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [8, "status", "System-Component-Status", [], "Describes the operational status of the system component."],
          [9, "responsible-roles", "Responsible-roles", ["[0"], "A reference to a role with responsibility for performing a function relative to the containing object, optionally associated with a set of persons and/or organizations that perform that role."],
          [10, "protocols", "Protocols", ["[0"], "Information about the protocol used to provide a service."],
          [11, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["System-component$type", "Choice", [], "A category describing the purpose of the component.", [
          [1, "c1", "StringDatatype", [], ""],
          [2, "c2", "System-component$type$2", [], ""]
        ]],

        ["System-component$type$2", "Enumerated", [], "", [
          [1, "this-system", ""],
          [2, "system", ""],
          [3, "interconnection", ""],
          [4, "software", ""],
          [5, "hardware", ""],
          [6, "service", ""],
          [7, "policy", ""],
          [8, "physical", ""],
          [9, "process-procedure", ""],
          [10, "plan", ""],
          [11, "guidance", ""],
          [12, "standard", ""],
          [13, "validation", ""],
          [14, "network", ""]
        ]],

        ["System-Component-Status", "Record", [], "Describes the operational status of the system component.", [
            [1, "state", "TokenDatatype", ["[1", "]1"], "The operational status."],
            [2, "remarks", "String", ["[0", "]1"], "Additional commentary about the containing object."]
        ]],

        ["Responsible-roles", "ArrayOf", ["{1", "*Responsible-role"], "", []],

        ["Protocols", "ArrayOf", ["{1", "*Protocol"], "", []],

        ["Protocol", "Record", [], "Information about the protocol used to provide a service.", [
          [1, "uuid", "UUIDDatatype", ["[0"], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this service protocol information elsewhere in this or other OSCAL instances. The locally defined UUID of the service protocol can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "name", "StringDatatype", [], "The common name of the protocol, which should be the appropriate \"service name\" from the IANA Service Name and Transport Protocol Port Number Registry."],
          [3, "title", "String", ["[0"], "A human readable name for the protocol (e.g., Transport Layer Security)."],
          [4, "port-ranges", "Port-ranges", ["[0"], "Where applicable this is the IPv4 port range on which the service operates."]
        ]],

        ["Port-ranges", "ArrayOf", ["{1", "*Port-range"], "", []],

        ["Port-range", "Record", [], "Where applicable this is the IPv4 port range on which the service operates.", [
          [1, "start", "NonNegativeIntegerDatatype", ["[0"], "Indicates the starting port number in a port range"],
          [2, "end", "NonNegativeIntegerDatatype", ["[0"], "Indicates the ending port number in a port range"],
          [3, "transport", "Port-range$transport", ["[0"], "Indicates the transport type."]
        ]],

        ["Port-range$transport", "Choice", [], "Indicates the transport type.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Port-range$transport$2", [], ""]
        ]],

        ["Port-range$transport$2", "Enumerated", [], "", [
          [1, "TCP", ""],
          [2, "UDP", ""]
        ]],

        ["Implementation-status", "Record", [], "Indicates the degree to which the a given control is implemented.", [
          [1, "state", "Implementation-status$state", [], "Identifies the implementation status of the control or control objective."],
          [2, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Implementation-status$state", "Choice", [], "Identifies the implementation status of the control or control objective.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Implementation-status$state$2", [], ""]
        ]],

        ["Implementation-status$state$2", "Enumerated", [], "", [
          [1, "implemented", ""],
          [2, "partial", ""],
          [3, "planned", ""],
          [4, "alternative", ""],
          [5, "not-applicable", ""]
        ]],

        ["System-user", "Record", [], "A type of user that interacts with the system based on an associated role.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this user class elsewhere in this or other OSCAL instances. The locally defined UUID of the system user can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "title", "String", ["[0"], "A name given to the user, which may be used by a tool for display and navigation."],
          [3, "short-name", "StringDatatype", ["[0"], "A short common name, abbreviation, or acronym for the user."],
          [4, "description", "String", ["[0"], "A summary of the user's purpose within the system."],
          [5, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [6, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [7, "role-ids", "Role-ids", ["[0"], "Reference to a role by UUID."],
          [8, "authorized-privileges", "Authorized-privileges", ["[0"], "Identifies a specific system privilege held by the user, along with an associated description and/or rationale for the privilege."],
          [9, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Role-ids", "ArrayOf", ["{1", "*TokenDatatype"], "", []],

        ["Authorized-privileges", "ArrayOf", ["{1", "*Authorized-privilege"], "", []],

        ["Authorized-privilege", "Record", [], "Identifies a specific system privilege held by the user, along with an associated description and/or rationale for the privilege.", [
          [1, "title", "String", [], "A human readable name for the privilege."],
          [2, "description", "String", ["[0"], "A summary of the privilege's purpose within the system."],
          [3, "functions-performed", "Functions-performed", [], "Describes a function performed for a given authorized privilege by this user class."]
        ]],

        ["Functions-performed", "ArrayOf", ["{1", "*StringDatatype"], "", []],

        ["Inventory-item", "Record", [], "A single managed inventory item within the system.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this inventory item elsewhere in this or other OSCAL instances. The locally defined UUID of the inventory item can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "description", "String", [], "A summary of the inventory item stating its purpose within the system."],
          [3, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [4, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [5, "responsible-parties", "Responsible-parties", ["[0"], "A reference to a set of persons and/or organizations that have responsibility for performing the referenced role in the context of the containing object."],
          [6, "implemented-components", "Implemented-components", ["[0"], "The set of components that are implemented in a given system inventory item."],
          [7, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Implemented-components", "ArrayOf", ["{1", "*Implemented-component"], "", []],

        ["Implemented-component", "Record", [], "The set of components that are implemented in a given system inventory item.", [
          [1, "component-uuid", "UUIDDatatype", [], "A machine-oriented identifier reference to a component that is implemented as part of an inventory item."],
          [2, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [3, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [4, "responsible-parties", "Responsible-parties", ["[0"], "A reference to a set of persons and/or organizations that have responsibility for performing the referenced role in the context of the containing object."],
          [5, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Set-parameter", "Record", [], "Identifies the parameter that will be set by the enclosed value.", [
          [1, "param-id", "TokenDatatype", [], "A human-oriented reference to a parameter within a control, who's catalog has been imported into the current implementation context."],
          [2, "values", "Values", [], "A parameter value or set of values."],
          [3, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Values", "ArrayOf", ["{1", "*StringDatatype"], "", []],

        ["System-id", "Record", [], "A human-oriented, globally unique identifier with cross-instance scope that can be used to reference this system identification property elsewhere in this or other OSCAL instances. When referencing an externally defined system identification, the system identification must be used in the context of the external / imported OSCAL instance (e.g., uri-reference). This string should be assigned per-subject, which means it should be consistently used to identify the same system across revisions of the document.", [
          [1, "identifier-type", "System-id$identifier-type", ["[0"], "Identifies the identification system from which the provided identifier was assigned."],
          [2, "id", "StringDatatype", [], ""]
        ]],

        ["System-id$identifier-type", "Choice", [], "Identifies the identification system from which the provided identifier was assigned.", [
          [1, "c1", "URIDatatype", [], ""],
          [2, "c2", "System-id$identifier-type$2", [], ""]
        ]],

        ["System-id$identifier-type$2", "Enumerated", [], "", [
          [1, "https://fedramp.gov", ""],
          [2, "http://fedramp.gov/ns/oscal", ""],
          [3, "https://ietf.org/rfc/rfc4122", ""],
          [4, "http://ietf.org/rfc/rfc4122", ""]
        ]],

        ["Part", "Record", [], "An annotated, markup-based textual element of a control's or catalog group's definition, or a child of another part.", [
          [1, "id", "TokenDatatype", ["[0"], "A unique identifier for the part."],
          [2, "name", "TokenDatatype", [], "A textual label that uniquely identifies the part's semantic type, which exists in a value space qualified by the ns."],
          [3, "ns", "URIDatatype", ["[0"], "An optional namespace qualifying the part's name. This allows different organizations to associate distinct semantics with the same name."],
          [4, "class", "TokenDatatype", ["[0"], "An optional textual providing a sub-type or characterization of the part's name, or a category to which the part belongs."],
          [5, "title", "String", ["[0"], "An optional name given to the part, which may be used by a tool for display and navigation."],
          [6, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [7, "prose", "String", ["[0"], "Permits multiple paragraphs, lists, tables etc."],
          [8, "parts", "Control-Parts", ["[0"], "An annotated, markup-based textual element of a control's or catalog group's definition, or a child of another part."],
          [9, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."]
        ]],

        ["Control-Parts", "ArrayOf", ["{1", "*Part"], "", []],

        ["Parameter", "Record", [], "Parameters provide a mechanism for the dynamic assignment of value(s) in a control.", [
          [1, "id", "TokenDatatype", [], "A unique identifier for the parameter."],
          [2, "class", "TokenDatatype", ["[0"], "A textual label that provides a characterization of the type, purpose, use or scope of the parameter."],
          [3, "depends-on", "TokenDatatype", ["[0"], "(deprecated) Another parameter invoking this one. This construct has been deprecated and should not be used."],
          [4, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [5, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [6, "label", "String", ["[0"], "A short, placeholder name for the parameter, which can be used as a substitute for a value if no value is assigned."],
          [7, "usage", "String", ["[0"], "Describes the purpose and use of a parameter."],
          [8, "constraints", "Constraints", ["[0"], "A formal or informal expression of a constraint or test."],
          [9, "guidelines", "Guidelines", ["[0"], "A prose statement that provides a recommendation for the use of a parameter."],
          [10, "values", "Values", ["[0"], "A parameter value or set of values."],
          [11, "select", "Parameter-selection", ["[0"], "Presenting a choice among alternatives."],
          [12, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Constraints", "ArrayOf", ["{1", "*Parameter-constraint"], "", []],

        ["Guidelines", "ArrayOf", ["{1", "*Parameter-guideline"], "", []],

        ["Parameter-constraint", "Record", [], "A formal or informal expression of a constraint or test.", [
          [1, "description", "String", ["[0"], "A textual summary of the constraint to be applied."],
          [2, "tests", "Tests", ["[0"], "A test expression which is expected to be evaluated by a tool."]
        ]],

        ["Tests", "ArrayOf", ["{1", "*Test"], "", []],

        ["Test", "Record", [], "A test expression which is expected to be evaluated by a tool.", [
          [1, "expression", "StringDatatype", [], "A formal (executable) expression of a constraint."],
          [2, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Parameter-guideline", "Record", [], "A prose statement that provides a recommendation for the use of a parameter.", [
          [1, "prose", "String", [], "Prose permits multiple paragraphs, lists, tables etc."]
        ]],

        ["Parameter-selection", "Record", [], "Presenting a choice among alternatives.", [
          [1, "how-many", "Parameter-selection$how-many", ["[0"], "Describes the number of selections that must occur. Without this setting, only one value should be assumed to be permitted."],
          [2, "choice", "Choice1", ["[0"], "A value selection among several such options."]
        ]],

        ["Parameter-selection$how-many", "Choice", [], "Describes the number of selections that must occur. Without this setting, only one value should be assumed to be permitted.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Parameter-selection$how-many$2", [], ""]
        ]],

        ["Parameter-selection$how-many$2", "Enumerated", [], "", [
          [1, "one", ""],
          [2, "one-or-more", ""]
        ]],

        ["Choice1", "ArrayOf", ["{1", "*String"], "", []],

        ["Choice1-item", "String", [], "A value selection among several such options.", []],

        ["Include-all", "Record", [], "Include all controls from the imported catalog or profile resources.", []],

        ["Import-ssp", "Record", [], "Used by the assessment plan and POA&M to import information about the system.", [
          [1, "href", "URIReferenceDatatype", [], "A resolvable URL reference to the system security plan for the system being assessed."],
          [2, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Local-objective", "Record", [], "A local definition of a control objective for this assessment. Uses catalog syntax for control objective and assessment actions.", [
          [1, "control-id", "TokenDatatype", [], "A reference to a control with a corresponding id value. When referencing an externally defined control, the Control Identifier Reference must be used in the context of the external / imported OSCAL instance (e.g., uri-reference)."],
          [2, "description", "String", ["[0"], "A human-readable description of this control objective."],
          [3, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [4, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [5, "parts", "Control-Parts", [], "An annotated, markup-based textual element of a control's or catalog group's definition, or a child of another part."],
          [6, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Assessment-method", "Record", [], "A local definition of a control objective. Uses catalog syntax for control objective and assessment activities.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this assessment method elsewhere in this or other OSCAL instances. The locally defined UUID of the assessment method can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "description", "String", ["[0"], "A human-readable description of this assessment method."],
          [3, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [4, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [5, "part", "Assessment-part", [], "A partition of an assessment plan or results or a child of another part."],
          [6, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Activity", "Record", [], "Identifies an assessment or related process that can be performed. In the assessment plan, this is an intended activity which may be associated with an assessment task. In the assessment results, this an activity that was actually performed as part of an assessment.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this assessment activity elsewhere in this or other OSCAL instances. The locally defined UUID of the activity can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "title", "String", ["[0"], "The title for this included activity."],
          [3, "description", "String", [], "A human-readable description of this included activity."],
          [4, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [5, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [6, "steps", "Steps", ["[0"], "Identifies an individual step in a series of steps related to an activity, such as an assessment test or examination procedure."],
          [7, "related-controls", "Reviewed-controls", ["[0"], "Identifies the controls being assessed and their control objectives."],
          [8, "responsible-roles", "Responsible-roles", ["[0"], "A reference to a role with responsibility for performing a function relative to the containing object, optionally associated with a set of persons and/or organizations that perform that role."],
          [9, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Steps", "ArrayOf", ["{1", "*Step"], "", []],

        ["Step", "Record", [], "Identifies an individual step in a series of steps related to an activity, such as an assessment test or examination procedure.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this step elsewhere in this or other OSCAL instances. The locally defined UUID of the step (in a series of steps) can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "title", "String", ["[0"], "The title for this step."],
          [3, "description", "String", [], "A human-readable description of this step."],
          [4, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [5, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [6, "reviewed-controls", "Reviewed-controls", ["[0"], "Identifies the controls being assessed and their control objectives."],
          [7, "responsible-roles", "Responsible-roles", ["[0"], "A reference to a role with responsibility for performing a function relative to the containing object, optionally associated with a set of persons and/or organizations that perform that role."],
          [8, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Task", "Record", [], "Represents a scheduled event or milestone, which may be associated with a series of assessment actions.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this task elsewhere in this or other OSCAL instances. The locally defined UUID of the task can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "type", "Task$type", [], "The type of task."],
          [3, "title", "String", [], "The title for this task."],
          [4, "description", "String", ["[0"], "A human-readable description of this task."],
          [5, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [6, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [7, "timing", "Task-Timing", ["[0"], "The timing under which the task is intended to occur."],
          [8, "dependencies", "Dependencies", ["[0"], "Used to indicate that a task is dependent on another task."],
          [9, "tasks", "Tasks", ["[0"], "Represents a scheduled event or milestone, which may be associated with a series of assessment actions."],
          [10, "associated-activities", "Associated-activities", ["[0"], "Identifies an individual activity to be performed as part of a task."],
          [11, "subjects", "Assessment-Subjects", ["[0"], "Identifies system elements being assessed, such as components, inventory items, and locations. In the assessment plan, this identifies a planned assessment subject. In the assessment results this is an actual assessment subject, and reflects any changes from the plan. exactly what will be the focus of this assessment. Any subjects not identified in this way are out-of-scope."],
          [12, "responsible-roles", "Responsible-roles", ["[0"], "A reference to a role with responsibility for performing a function relative to the containing object, optionally associated with a set of persons and/or organizations that perform that role."],
          [13, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Task$type", "Choice", [], "The type of task.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Task$type$2", [], ""]
        ]],

        ["Task$type$2", "Enumerated", [], "", [
          [1, "milestone", ""],
          [2, "action", ""]
        ]],

        ["Task-Timing", "Choice", [], "", [
            [1, "on-date", "DateTimeWithTimezoneDatatype", [], ""],
            [2, "within-date-range", "Date-Range", [], ""],
            [3, "at-frequency", "Frequency-Condition", [], ""]
          ]],
        ["Date-Range", "Record", [], "The task is intended to occur within the specified date range.", [
            [1, "start", "DateTimeWithTimezoneDatatype", ["[1"], "The task must occur on or after the specified date."],
            [2, "end", "DateTimeWithTimezoneDatatype", ["[1"], "The task must occur on or before the specified date."]
          ]],
        ["Frequency-Condition", "Record", [], "", [
            [1, "period", "PositiveIntegerDatatype", ["[1"], ""],
            [2, "unit", "String", ["[1"], ""]
          ]],

        ["Dependencies", "ArrayOf", ["{1", "*Dependency"], "", []],

        ["Dependency", "Record", [], "Used to indicate that a task is dependent on another task.", [
          [1, "task-uuid", "UUIDDatatype", [], "A machine-oriented identifier reference to a unique task."],
          [2, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Tasks", "ArrayOf", ["{1", "*Task"], "", []],

        ["Associated-activities", "ArrayOf", ["{1", "*Associated-activity"], "", []],

        ["Associated-activity", "Record", [], "Identifies an individual activity to be performed as part of a task.", [
          [1, "activity-uuid", "UUIDDatatype", [], "A machine-oriented identifier reference to an activity defined in the list of activities."],
          [2, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [3, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [4, "responsible-roles", "Responsible-roles", ["[0"], "A reference to a role with responsibility for performing a function relative to the containing object, optionally associated with a set of persons and/or organizations that perform that role."],
          [5, "subjects", "Assessment-Subjects", [], "Identifies system elements being assessed, such as components, inventory items, and locations. In the assessment plan, this identifies a planned assessment subject. In the assessment results this is an actual assessment subject, and reflects any changes from the plan. exactly what will be the focus of this assessment. Any subjects not identified in this way are out-of-scope."],
          [6, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Assessment-Subjects", "ArrayOf", ["{1", "*Assessment-subject"], "", []],

        ["Reviewed-controls", "Record", [], "Identifies the controls being assessed and their control objectives.", [
          [1, "description", "String", ["[0"], "A human-readable description of control objectives."],
          [2, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [3, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [4, "control-selections", "Control-selections", [], "Identifies the controls being assessed. In the assessment plan, these are the planned controls. In the assessment results, these are the actual controls, and reflects any changes from the plan."],
          [5, "control-objective-selections", "Control-objective-selections", ["[0"], "Identifies the control objectives of the assessment. In the assessment plan, these are the planned objectives. In the assessment results, these are the assessed objectives, and reflects any changes from the plan."],
          [6, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Control-selections", "ArrayOf", ["{1", "*Control-selection"], "", []],

        ["Control-selection", "Record", [], "Identifies the controls being assessed. In the assessment plan, these are the planned controls. In the assessment results, these are the actual controls, and reflects any changes from the plan.", [
          [1, "description", "String", ["[0"], "A human-readable description of in-scope controls specified for assessment."],
          [2, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [3, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [4, "include-all", "Include-all", ["[0"], "Include all controls from the imported catalog or profile resources."],
          [5, "include-controls", "Include-controls", ["[0"], "Used to select a control for inclusion/exclusion based on one or more control identifiers. A set of statement identifiers can be used to target the inclusion/exclusion to only specific control statements providing more granularity over the specific statements that are within the asessment scope."],
          [6, "exclude-controls", "Exclude-controls", ["[0"], "Used to select a control for inclusion/exclusion based on one or more control identifiers. A set of statement identifiers can be used to target the inclusion/exclusion to only specific control statements providing more granularity over the specific statements that are within the asessment scope."],
          [7, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Include-controls", "ArrayOf", ["{1", "*Select-control-by-id"], "", []],

        ["Exclude-controls", "ArrayOf", ["{1", "*Select-control-by-id"], "", []],

        ["Control-objective-selections", "ArrayOf", ["{1", "*Control-objective-selection"], "", []],

        ["Control-objective-selection", "Record", [], "Identifies the control objectives of the assessment. In the assessment plan, these are the planned objectives. In the assessment results, these are the assessed objectives, and reflects any changes from the plan.", [
          [1, "description", "String", ["[0"], "A human-readable description of this collection of control objectives."],
          [2, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [3, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [4, "include-all", "Include-all", ["[0"], "Include all controls from the imported catalog or profile resources."],
          [5, "include-objectives", "Include-objectives", ["[0"], "Used to select a control objective for inclusion/exclusion based on the control objective's identifier."],
          [6, "exclude-objectives", "Exclude-objectives", ["[0"], "Used to select a control objective for inclusion/exclusion based on the control objective's identifier."],
          [7, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Include-objectives", "ArrayOf", ["{1", "*Select-objective-by-id"], "", []],

        ["Exclude-objectives", "ArrayOf", ["{1", "*Select-objective-by-id"], "", []],

        ["Select-control-by-id", "Record", [], "Used to select a control for inclusion/exclusion based on one or more control identifiers. A set of statement identifiers can be used to target the inclusion/exclusion to only specific control statements providing more granularity over the specific statements that are within the asessment scope.", [
          [1, "control-id", "TokenDatatype", [], "A reference to a control with a corresponding id value. When referencing an externally defined control, the Control Identifier Reference must be used in the context of the external / imported OSCAL instance (e.g., uri-reference)."],
          [2, "statement-ids", "Statement-ids", ["[0"], "Used to constrain the selection to only specificity identified statements."]
        ]],

        ["Statement-ids", "ArrayOf", ["{1", "*TokenDatatype"], "", []],

        ["Select-objective-by-id", "Record", [], "Used to select a control objective for inclusion/exclusion based on the control objective's identifier.", [
          [1, "objective-id", "TokenDatatype", [], "Points to an assessment objective."]
        ]],

        ["Assessment-subject-placeholder", "Record", [], "Used when the assessment subjects will be determined as part of one or more other assessment activities. These assessment subjects will be recorded in the assessment results in the assessment log.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier for a set of assessment subjects that will be identified by a task or an activity that is part of a task. The locally defined UUID of the assessment subject placeholder can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "description", "String", ["[0"], "A human-readable description of intent of this assessment subject placeholder."],
          [3, "sources", "Sources", [], "Assessment subjects will be identified while conducting the referenced activity-instance."],
          [4, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [5, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [6, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Sources", "ArrayOf", ["{1", "*Source"], "", []],

        ["Source", "Record", [], "Assessment subjects will be identified while conducting the referenced activity-instance.", [
          [1, "task-uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference (in this or other OSCAL instances) an assessment activity to be performed as part of the event. The locally defined UUID of the task can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."]
        ]],

        ["Assessment-subject", "Record", [], "Identifies system elements being assessed, such as components, inventory items, and locations. In the assessment plan, this identifies a planned assessment subject. In the assessment results this is an actual assessment subject, and reflects any changes from the plan. exactly what will be the focus of this assessment. Any subjects not identified in this way are out-of-scope.", [
          [1, "type", "Assessment-subject$type", [], "Indicates the type of assessment subject, such as a component, inventory, item, location, or party represented by this selection statement."],
          [2, "description", "String", ["[0"], "A human-readable description of the collection of subjects being included in this assessment."],
          [3, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [4, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [5, "include-all", "Include-all", ["[0"], "Include all controls from the imported catalog or profile resources."],
          [6, "include-subjects", "Include-subjects", ["[0"], "Identifies a set of assessment subjects to include/exclude by UUID."],
          [7, "exclude-subjects", "Exclude-subjects", ["[0"], "Identifies a set of assessment subjects to include/exclude by UUID."],
          [8, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Assessment-subject$type", "Choice", [], "Indicates the type of assessment subject, such as a component, inventory, item, location, or party represented by this selection statement.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Assessment-subject$type$2", [], ""]
        ]],

        ["Assessment-subject$type$2", "Enumerated", [], "", [
          [1, "component", ""],
          [2, "inventory-item", ""],
          [3, "location", ""],
          [4, "party", ""],
          [5, "user", ""]
        ]],

        ["Include-subjects", "ArrayOf", ["{1", "*Select-subject-by-id"], "", []],

        ["Exclude-subjects", "ArrayOf", ["{1", "*Select-subject-by-id"], "", []],

        ["Select-subject-by-id", "Record", [], "Identifies a set of assessment subjects to include/exclude by UUID.", [
          [1, "subject-uuid", "UUIDDatatype", [], "A machine-oriented identifier reference to a component, inventory-item, location, party, user, or resource using it's UUID."],
          [2, "type", "Select-subject-by-id$type", [], "Used to indicate the type of object pointed to by the uuid-ref within a subject."],
          [3, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [4, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [5, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Select-subject-by-id$type", "Choice", [], "Used to indicate the type of object pointed to by the uuid-ref within a subject.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Select-subject-by-id$type$2", [], ""]
        ]],

        ["Select-subject-by-id$type$2", "Enumerated", [], "", [
          [1, "component", ""],
          [2, "inventory-item", ""],
          [3, "location", ""],
          [4, "party", ""],
          [5, "user", ""],
          [6, "resource", ""]
        ]],

        ["Subject-reference", "Record", [], "A human-oriented identifier reference to a resource. Use type to indicate whether the identified resource is a component, inventory item, location, user, or something else.", [
          [1, "subject-uuid", "UUIDDatatype", [], "A machine-oriented identifier reference to a component, inventory-item, location, party, user, or resource using it's UUID."],
          [2, "type", "Subject-reference$type", [], "Used to indicate the type of object pointed to by the uuid-ref within a subject."],
          [3, "title", "String", ["[0"], "The title or name for the referenced subject."],
          [4, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [5, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [6, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Subject-reference$type", "Choice", [], "Used to indicate the type of object pointed to by the uuid-ref within a subject.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Subject-reference$type$2", [], ""]
        ]],

        ["Subject-reference$type$2", "Enumerated", [], "", [
          [1, "component", ""],
          [2, "inventory-item", ""],
          [3, "location", ""],
          [4, "party", ""],
          [5, "user", ""],
          [6, "resource", ""]
        ]],

        ["Assessment-assets", "Record", [], "Identifies the assets used to perform this assessment, such as the assessment team, scanning tools, and assumptions.", [
          [1, "components", "Components", ["[0"], "A defined component that can be part of an implemented system."],
          [2, "assessment-platforms", "Assessment-platforms", [], "Used to represent the toolset used to perform aspects of the assessment."]
        ]],

        ["Assessment-platforms", "ArrayOf", ["{1", "*Assessment-platform"], "", []],

        ["Assessment-platform", "Record", [], "Used to represent the toolset used to perform aspects of the assessment.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this assessment platform elsewhere in this or other OSCAL instances. The locally defined UUID of the assessment platform can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "title", "String", ["[0"], "The title or name for the assessment platform."],
          [3, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [4, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [5, "uses-components", "Uses-components", ["[0"], "The set of components that are used by the assessment platform."],
          [6, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Uses-components", "ArrayOf", ["{1", "*Uses-component"], "", []],

        ["Uses-component", "Record", [], "The set of components that are used by the assessment platform.", [
          [1, "component-uuid", "UUIDDatatype", [], "A machine-oriented identifier reference to a component that is implemented as part of an inventory item."],
          [2, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [3, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [4, "responsible-parties", "Responsible-parties", ["[0"], "A reference to a set of persons and/or organizations that have responsibility for performing the referenced role in the context of the containing object."],
          [5, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Finding-target", "Record", [], "Captures an assessor's conclusions regarding the degree to which an objective is satisfied.", [
          [1, "type", "Finding-target$type", [], "Identifies the type of the target."],
          [2, "target-id", "TokenDatatype", [], "A machine-oriented identifier reference for a specific target qualified by the type."],
          [3, "title", "String", ["[0"], "The title for this objective status."],
          [4, "description", "String", ["[0"], "A human-readable description of the assessor's conclusions regarding the degree to which an objective is satisfied."],
          [5, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [6, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [7, "status", "Finding-Target-Status", [], "A determination of if the objective is satisfied or not within a given system."],
          [8, "implementation-status", "Implementation-status", ["[0"], "Indicates the degree to which the a given control is implemented."],
          [9, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Finding-target$type", "Choice", [], "Identifies the type of the target.", [
          [1, "c1", "StringDatatype", [], ""],
          [2, "c2", "Finding-target$type$2", [], ""]
        ]],

        ["Finding-target$type$2", "Enumerated", [], "", [
          [1, "statement-id", ""],
          [2, "objective-id", ""]
        ]],

        ["Finding-Target-Status", "Record", [], "A determination of if the objective is satisfied or not within a given system.", [
            [1, "state", "TokenDatatype", ["[1"], "An indication as to whether the objective is satisfied or not."],
            [2, "reason", "TokenDatatype", ["[0"], "The reason the objective was given it's status."],
            [3, "remarks", "String", ["[0", "]1"], "Additional commentary about the containing object."]
        ]],

        ["Finding", "Record", [], "Describes an individual finding.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this finding in this or other OSCAL instances. The locally defined UUID of the finding can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "title", "String", [], "The title for this finding."],
          [3, "description", "String", [], "A human-readable description of this finding."],
          [4, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [5, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [6, "origins", "Origins", ["[0"], "Identifies the source of the finding, such as a tool, interviewed person, or activity."],
          [7, "target", "Finding-target", [], "Captures an assessor's conclusions regarding the degree to which an objective is satisfied."],
          [8, "implementation-statement-uuid", "UUIDDatatype", ["[0"], "A machine-oriented identifier reference to the implementation statement in the SSP to which this finding is related."],
          [9, "related-observations", "Related-observations", ["[0"], "Relates the finding to a set of referenced observations that were used to determine the finding."],
          [10, "related-risks", "Related-risks", ["[0"], "Relates the finding to a set of referenced risks that were used to determine the finding."],
          [11, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Observation", "Record", [], "Describes an individual observation.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this observation elsewhere in this or other OSCAL instances. The locally defined UUID of the observation can be used to reference the data item locally or globally (e.g., in an imorted OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "title", "String", ["[0"], "The title for this observation."],
          [3, "description", "String", [], "A human-readable description of this assessment observation."],
          [4, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [5, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [6, "methods", "Methods", [], "Identifies how the observation was made."],
          [7, "types", "Types", ["[0"], "Identifies the nature of the observation. More than one may be used to further qualify and enable filtering."],
          [8, "origins", "Origins", ["[0"], "Identifies the source of the finding, such as a tool, interviewed person, or activity."],
          [9, "subjects", "Subject-refs", ["[0"], "A human-oriented identifier reference to a resource. Use type to indicate whether the identified resource is a component, inventory item, location, user, or something else."],
          [10, "relevant-evidence", "Relevant-evidence", ["[0"], "Links this observation to relevant evidence."],
          [11, "collected", "DateTimeWithTimezoneDatatype", [], "Date/time stamp identifying when the finding information was collected."],
          [12, "expires", "DateTimeWithTimezoneDatatype", ["[0"], "Date/time identifying when the finding information is out-of-date and no longer valid. Typically used with continuous assessment scenarios."],
          [13, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Methods", "ArrayOf", ["{1", "*Method"], "", []],

        ["Method", "Choice", [], "Identifies how the observation was made.", [
          [1, "c1", "StringDatatype", [], ""],
          [2, "c2", "Method$2", [], ""]
        ]],

        ["Method$2", "Enumerated", [], "", [
          [1, "EXAMINE", ""],
          [2, "INTERVIEW", ""],
          [3, "TEST", ""],
          [4, "UNKNOWN", ""]
        ]],

        ["Types", "ArrayOf", ["{1", "*Type"], "", []],

        ["Type", "Choice", [], "Identifies the nature of the observation. More than one may be used to further qualify and enable filtering.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Type$2", [], ""]
        ]],

        ["Type$2", "Enumerated", [], "", [
          [1, "ssp-statement-issue", ""],
          [2, "control-objective", ""],
          [3, "mitigation", ""],
          [4, "finding", ""],
          [5, "historic", ""]
        ]],

        ["Subject-refs", "ArrayOf", ["{1", "*Subject-reference"], "", []],

        ["Relevant-evidence", "ArrayOf", ["{1", "*Relevant-evidence-item"], "", []],

        ["Relevant-evidence-item", "Record", [], "Links this observation to relevant evidence.", [
          [1, "href", "URIReferenceDatatype", ["[0"], "A resolvable URL reference to relevant evidence."],
          [2, "description", "String", [], "A human-readable description of this evidence."],
          [3, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [4, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [5, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Origin", "Record", [], "Identifies the source of the finding, such as a tool, interviewed person, or activity.", [
          [1, "actors", "Actors", [], "The actor that produces an observation, a finding, or a risk. One or more actor type can be used to specify a person that is using a tool."],
          [2, "related-tasks", "Related-tasks", ["[0"], "Identifies an individual task for which the containing object is a consequence of."]
        ]],

        ["Related-tasks", "ArrayOf", ["{1", "*Related-task"], "", []],

        ["Origin-actor", "Record", [], "The actor that produces an observation, a finding, or a risk. One or more actor type can be used to specify a person that is using a tool.", [
          [1, "type", "Origin-actor$type", [], "The kind of actor."],
          [2, "actor-uuid", "UUIDDatatype", [], "A machine-oriented identifier reference to the tool or person based on the associated type."],
          [3, "role-id", "TokenDatatype", ["[0"], "For a party, this can optionally be used to specify the role the actor was performing."],
          [4, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [5, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."]
        ]],

        ["Origin-actor$type", "Choice", [], "The kind of actor.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Origin-actor$type$2", [], ""]
        ]],

        ["Origin-actor$type$2", "Enumerated", [], "", [
          [1, "tool", ""],
          [2, "assessment-platform", ""],
          [3, "party", ""]
        ]],

        ["Related-task", "Record", [], "Identifies an individual task for which the containing object is a consequence of.", [
          [1, "task-uuid", "UUIDDatatype", [], "A machine-oriented identifier reference to a unique task."],
          [2, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [3, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [4, "responsible-parties", "Responsible-parties", ["[0"], "A reference to a set of persons and/or organizations that have responsibility for performing the referenced role in the context of the containing object."],
          [5, "subjects", "Assessment-Subjects", ["[0"], "Identifies system elements being assessed, such as components, inventory items, and locations. In the assessment plan, this identifies a planned assessment subject. In the assessment results this is an actual assessment subject, and reflects any changes from the plan. exactly what will be the focus of this assessment. Any subjects not identified in this way are out-of-scope."],
          [6, "identified-subject", "Identified-Subject", ["[0"], "Used to detail assessment subjects that were identfied by this task."],
          [7, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Identified-Subject", "Record", [], "Used to detail assessment subjects that were identfied by this task.", [
            [1, "subject", "Assessment-Subjects", [], "Used to detail assessment subjects that were identfied by this task."],
            [2, "subject-placeholder-uuid", "UUIDDatatype", ["[1"], "Assessment Subject Placeholder Universally Unique Identifier Reference. A machine-oriented identifier reference to a unique assessment subject placeholder defined by this task."]
        ]],

        ["Threat-id", "Record", [], "A pointer, by ID, to an externally-defined threat.", [
          [1, "system", "Threat-id$system", [], "Specifies the source of the threat information."],
          [2, "href", "URIReferenceDatatype", ["[0"], "An optional location for the threat data, from which this ID originates."],
          [3, "id", "URIDatatype", [], ""]
        ]],

        ["Threat-id$system", "Choice", [], "Specifies the source of the threat information.", [
          [1, "c1", "URIDatatype", [], ""],
          [2, "c2", "Threat-id$system$2", [], ""]
        ]],

        ["Threat-id$system$2", "Enumerated", [], "", [
          [1, "http://fedramp.gov", ""],
          [2, "http://fedramp.gov/ns/oscal", ""]
        ]],

        ["Risk", "Record", [], "An identified risk.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this risk elsewhere in this or other OSCAL instances. The locally defined UUID of the risk can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "title", "String", [], "The title for this risk."],
          [3, "description", "String", [], "A human-readable summary of the identified risk, to include a statement of how the risk impacts the system."],
          [4, "statement", "String", [], "An summary of impact for how the risk affects the system."],
          [5, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [6, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [7, "status", "Risk-status", [], "Describes the status of the associated risk."],
          [8, "origins", "Origins", ["[0"], "Identifies the source of the finding, such as a tool, interviewed person, or activity."],
          [9, "threat-ids", "Threat-ids", ["[0"], "A pointer, by ID, to an externally-defined threat."],
          [10, "characterizations", "Characterizations", ["[0"], "A collection of descriptive data about the containing object from a specific origin."],
          [11, "mitigating-factors", "Mitigating-factors", ["[0"], "Describes an existing mitigating factor that may affect the overall determination of the risk, with an optional link to an implementation statement in the SSP."],
          [12, "deadline", "DateTimeWithTimezoneDatatype", ["[0"], "The date/time by which the risk must be resolved."],
          [13, "remediations", "Remediations", ["[0"], "Describes either recommended or an actual plan for addressing the risk."],
          [14, "risk-log", "ArrayOf", ["*Risk-Log-Entry", "[0"], "A log of all risk-related tasks taken."],
          [15, "related-observations", "Related-observations", ["[0"], "Relates the finding to a set of referenced observations that were used to determine the finding."]
        ]],

        ["Threat-ids", "ArrayOf", ["{1", "*Threat-id"], "", []],

        ["Characterizations", "ArrayOf", ["{1", "*Characterization"], "", []],

        ["Mitigating-factors", "ArrayOf", ["{1", "*Mitigating-factor"], "", []],

        ["Mitigating-factor", "Record", [], "Describes an existing mitigating factor that may affect the overall determination of the risk, with an optional link to an implementation statement in the SSP.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this mitigating factor elsewhere in this or other OSCAL instances. The locally defined UUID of the mitigating factor can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "implementation-uuid", "UUIDDatatype", ["[0"], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this implementation statement elsewhere in this or other OSCAL instancess. The locally defined UUID of the implementation statement can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [3, "description", "String", [], "A human-readable description of this mitigating factor."],
          [4, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [5, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [6, "subjects", "Subject-refs", ["[0"], "A human-oriented identifier reference to a resource. Use type to indicate whether the identified resource is a component, inventory item, location, user, or something else."]
        ]],

        ["Risk-Log-Entry", "Record", [], "A log of all risk-related tasks taken.", [
          [1, "title", "String", ["[0", "]1"], "The title for this risk log entry."],
          [2, "description", "String", [], "A human-readable description of what was done regarding the risk."],        
          [3, "start", "DateTimeWithTimezoneDatatype", ["[1", "]1"], "Identifies the start date and time of the event."],
          [4, "end", "DateTimeWithTimezoneDatatype", [], "Identifies the end date and time of the event. If the event is a point in time, the start and end will be the same date and time."],    
          [5, "props", "Props", ["[0", "]1"], ""],
          [6, "links", "Links", [], ""],
          [7, "logged-by", "Logged-by", ["[0"], ""],
          [8, "status-change", "Risk-status", [], ""],
          [9, "related-responses", "ArrayOf", ["*related-response", "[0", "]0"], ""],
          [10, "remarks", "String", [], ""]
        ]],

        ["Logged-by", "Record", [], "Used to indicate who created a log entry in what role.", [
          [1, "party-uuid", "UUIDDatatype", [], "A machine-oriented identifier reference to the party who is making the log entry."],
          [2, "role-id", "TokenDatatype", ["[0"], "A point to the role-id of the role in which the party is making the log entry."]
        ]],

        ["Risk-status", "Choice", [], "Describes the status of the associated risk.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Risk-status$2", [], ""]
        ]],

        ["Risk-status$2", "Enumerated", [], "", [
          [1, "open", ""],
          [2, "investigating", ""],
          [3, "remediating", ""],
          [4, "deviation-requested", ""],
          [5, "deviation-approved", ""],
          [6, "closed", ""]
        ]],

        ["related-response", "Record", [], "Identifies an individual risk response that this log entry is for.", [
            [1, "props", "Props", ["[0"], ""],
            [2, "links", "Links", ["[0"], ""],
            [3, "related-tasks", "Related-tasks", [], ""],
            [4, "remarks", "String", [], ""],
            [5, "field_value_5", "String", [], ""]
        ]],

        ["Remediations", "ArrayOf", ["{1", "*Response"], "", []],

        ["Characterization", "Record", [], "A collection of descriptive data about the containing object from a specific origin.", [
          [1, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [2, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [3, "origin", "Origin", [], "Identifies the source of the finding, such as a tool, interviewed person, or activity."],
          [4, "facets", "Facets", [], "An individual characteristic that is part of a larger set produced by the same actor."]
        ]],

        ["Facets", "ArrayOf", ["{1", "*Facet"], "", []],

        ["Facet", "Record", [], "An individual characteristic that is part of a larger set produced by the same actor.", [
          [1, "name", "TokenDatatype", [], "The name of the risk metric within the specified system."],
          [2, "system", "Facet$system", [], "Specifies the naming system under which this risk metric is organized, which allows for the same names to be used in different systems controlled by different parties. This avoids the potential of a name clash."],
          [3, "value", "StringDatatype", [], "Indicates the value of the facet."],
          [4, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [5, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [6, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Facet$system", "Choice", [], "Specifies the naming system under which this risk metric is organized, which allows for the same names to be used in different systems controlled by different parties. This avoids the potential of a name clash.", [
          [1, "c1", "URIDatatype", [], ""],
          [2, "c2", "Facet$system$2", [], ""]
        ]],

        ["Facet$system$2", "Enumerated", [], "", [
          [1, "http://fedramp.gov", ""],
          [2, "http://fedramp.gov/ns/oscal", ""],
          [3, "http://csrc.nist.gov/ns/oscal", ""],
          [4, "http://csrc.nist.gov/ns/oscal/unknown", ""],
          [5, "http://cve.mitre.org", ""],
          [6, "http://www.first.org/cvss/v2.0", ""],
          [7, "http://www.first.org/cvss/v3.0", ""],
          [8, "http://www.first.org/cvss/v3.1", ""]
        ]],

        ["Response", "Record", [], "Describes either recommended or an actual plan for addressing the risk.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this remediation elsewhere in this or other OSCAL instances. The locally defined UUID of the risk response can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "lifecycle", "Response$lifecycle", [], "Identifies whether this is a recommendation, such as from an assessor or tool, or an actual plan accepted by the system owner."],
          [3, "title", "String", [], "The title for this response activity."],
          [4, "description", "String", [], "A human-readable description of this response plan."],
          [5, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [6, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [7, "origins", "Origins", ["[0"], "Identifies the source of the finding, such as a tool, interviewed person, or activity."],
          [8, "required-assets", "Required-assets", ["[0"], "Identifies an asset required to achieve remediation."],
          [9, "tasks", "Tasks", ["[0"], "Represents a scheduled event or milestone, which may be associated with a series of assessment actions."],
          [10, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Response$lifecycle", "Choice", [], "Identifies whether this is a recommendation, such as from an assessor or tool, or an actual plan accepted by the system owner.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Response$lifecycle$2", [], ""]
        ]],

        ["Response$lifecycle$2", "Enumerated", [], "", [
          [1, "recommendation", ""],
          [2, "planned", ""],
          [3, "completed", ""]
        ]],

        ["Required-assets", "ArrayOf", ["{1", "*Required-asset"], "", []],

        ["Required-asset", "Record", [], "Identifies an asset required to achieve remediation.", [
          [1, "uuid", "UUIDDatatype", [], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this required asset elsewhere in this or other OSCAL instances. The locally defined UUID of the asset can be used to reference the data item locally or globally (e.g., in an imported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "subjects", "Subject-refs", ["[0"], "A human-oriented identifier reference to a resource. Use type to indicate whether the identified resource is a component, inventory item, location, user, or something else."],
          [3, "title", "String", ["[0"], "The title for this required asset."],
          [4, "description", "String", [], "A human-readable description of this required asset."],
          [5, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [6, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."],
          [7, "remarks", "Remarks", ["[0"], "Additional commentary about the containing object."]
        ]],

        ["Assessment-part", "Record", [], "A partition of an assessment plan or results or a child of another part.", [
          [1, "uuid", "UUIDDatatype", ["[0"], "A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this part elsewhere in this or other OSCAL instances. The locally defined UUID of the part can be used to reference the data item locally or globally (e.g., in an ported OSCAL instance). This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."],
          [2, "name", "Assessment-part$name", [], "A textual label that uniquely identifies the part's semantic type."],
          [3, "ns", "URIDatatype", ["[0"], "A namespace qualifying the part's name. This allows different organizations to associate distinct semantics with the same name."],
          [4, "class", "TokenDatatype", ["[0"], "A textual label that provides a sub-type or characterization of the part's name. This can be used to further distinguish or discriminate between the semantics of multiple parts of the same control with the same name and ns."],
          [5, "title", "String", ["[0"], "A name given to the part, which may be used by a tool for display and navigation."],
          [6, "props", "Props", ["[0"], "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair."],
          [7, "prose", "String", ["[0"], "Permits multiple paragraphs, lists, tables etc."],
          [8, "parts", "Control-Parts", ["[0"], "A partition of an assessment plan or results or a child of another part."],
          [9, "links", "Links", ["[0"], "A reference to a local or remote resource, that has a specific relation to the containing object."]
        ]],

        ["Assessment-part$name", "Choice", [], "A textual label that uniquely identifies the part's semantic type.", [
          [1, "c1", "TokenDatatype", [], ""],
          [2, "c2", "Assessment-part$name$2", [], ""]
        ]],

        ["Assessment-part$name$2", "Enumerated", [], "", [
          [1, "asset", ""],
          [2, "method", ""],
          [3, "objective", ""]
        ]],

        ["Assessment-Parts", "ArrayOf", ["{1", "*Assessment-part"], "", []],

        ["Base64Datatype", "String", ["%^[0-9A-Za-z+/]+={0,2}$"], "Binary data encoded using the Base 64 encoding algorithm as defined by RFC4648.", []],

        ["DateTimeWithTimezoneDatatype", "String", ["%^(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\\.[0-9]+)?(Z|(-((0[0-9]|1[0-2]):00|0[39]:30)|\\+((0[0-9]|1[0-4]):00|(0[34569]|10):30|(0[58]|12):45)))$"], "A string representing a point in time with a required timezone.", []],

        ["EmailAddressDatatype", "Choice", [], "An email address string formatted according to RFC 6531.", [
          [1, "c1", "StringDatatype", [], ""],
          [2, "c2", "String", [], ""]
        ]],

        ["EmailAddressDatatype$2", "String", ["%^.+@.+$"], "", []],

        ["IntegerDatatype", "Integer", [], "A whole number value.", []],

        ["NonNegativeIntegerDatatype", "Choice", [], "An integer value that is equal to or greater than 0.", [
          [1, "c1", "IntegerDatatype", [], ""],
          [2, "c2", "Number", [], ""]
        ]],

        ["NonNegativeIntegerDatatype$2", "Number", [], "", []],

        ["PositiveIntegerDatatype", "Choice", [], "An integer value that is greater than 0.", [
          [1, "c1", "IntegerDatatype", [], ""],
          [2, "c2", "Number", [], ""]
        ]],

        ["PositiveIntegerDatatype$2", "Number", [], "", []],

        ["StringDatatype", "String", ["%^\\S(.*\\S)?$"], "A non-empty string with leading and trailing whitespace disallowed. Whitespace is: U+9, U+10, U+32 or [ \n\t]+", []],

        ["TokenDatatype", "String", ["%^(\\p{L}|_)(\\p{L}|\\p{N}|[.\\-_])*$"], "A non-colonized name as defined by XML Schema Part 2: Datatypes Second Edition. https://www.w3.org/TR/xmlschema11-2/#NCName.", []],

        ["URIDatatype", "String", ["%^[a-zA-Z][a-zA-Z0-9+\\-.]+:.+$"], "A universal resource identifier (URI) formatted according to RFC3986.", []],

        ["URIReferenceDatatype", "String", [], "A URI Reference, either a URI or a relative-reference, formatted according to section 4.1 of RFC3986.", []],

        ["UUIDDatatype", "String", ["%^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$"], "A type 4 ('random' or 'pseudorandom') or type 5 UUID per RFC 4122.", []]
      ]
    }


    
    
    valid_data_list = [ valid_data ]
    invalid_data_list = [

         {'SuitEnum': 10},'Aces', 10
         
         ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 


def test_ui_issue_09042025_2():
  data = {
  "meta": {
    "package": "http://oasis-open.org/openc2/oc2ls/v1.0.1",
    "version": "0",
    "title": "Language schema with errata",
    "description": "OpenC2 LS version 1.0 + errata",
    "roots": ["OpenC2-Command", "OpenC2-Response"],
    "config": {
      "$MaxBinary": 255,
      "$MaxString": 255,
      "$MaxElements": 100,
      "$Sys": ":",
      "$TypeName": "^[A-Z][-:A-Za-z0-9]{0,31}$",
      "$FieldName": "^[a-z][-_a-z0-9]{0,31}$",
      "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
    }
  },
  "types": [
    ["OpenC2-Command", "Record", [], "", [
      [1, "action", "Action", [], "The task or activity to be performed (i.e., the 'verb')."],
      [2, "target", "Target", [], "The object of the Action. The Action is performed on the Target."],
      [3, "args", "Args", ["[0"], "Additional information that applies to the Command."],
      [4, "actuator", "Actuator", ["[0"], "The subject of the Action. The Actuator executes the Action on the Target."],
      [5, "command_id", "String", ["[0"], "An identifier of this Command."]
    ]],
    ["OpenC2-Response", "Map", ["{1"], "", [
      [1, "status", "Status-Code", [], "An integer status code"],
      [2, "status_text", "String", ["[0"], "A free-form human-readable description of the Response status"],
      [3, "results", "Results", ["[0"], "Map of key:value pairs that contain additional results based on the invoking Command."]
    ]],
    ["Action", "Enumerated", [], "", [
      [1, "scan", "Systematic examination of some aspect of the entity or its environment."],
      [2, "locate", "Find an object physically, logically, functionally, or by organization."],
      [3, "query", "Initiate a request for information."],
      [6, "deny", "Prevent a certain event or action from completion, such as preventing a flow from reaching a destination or preventing access."],
      [7, "contain", "Isolate a file, process, or entity so that it cannot modify or access assets or processes."],
      [8, "allow", "Permit access to or execution of a Target."],
      [9, "start", "Initiate a process, application, system, or activity."],
      [10, "stop", "Halt a system or end an activity."],
      [11, "restart", "Stop then start a system or an activity."],
      [14, "cancel", "Invalidate a previously issued Action."],
      [15, "set", "Change a value, configuration, or state of a managed entity."],
      [16, "update", "Instruct a component to retrieve, install, process, and operate in accordance with a software update, reconfiguration, or other update."],
      [18, "redirect", "Change the flow of traffic to a destination other than its original destination."],
      [19, "create", "Add a new entity of a known type (e.g., data, files, directories)."],
      [20, "delete", "Remove an entity (e.g., data, files, flows)."],
      [22, "detonate", "Execute and observe the behavior of a Target (e.g., file, hyperlink) in an isolated environment."],
      [23, "restore", "Return a system to a previously known state."],
      [28, "copy", "Duplicate an object, file, data flow, or artifact."],
      [30, "investigate", "Task the recipient to aggregate and report information as it pertains to a security event or incident."],
      [32, "remediate", "Task the recipient to eliminate a vulnerability or attack point."]
    ]],
    ["Target", "Choice", [], "OpenC2 Target datatypes", [
      [1, "artifact", "Artifact", [], "An array of bytes representing a file-like object or a link to that object."],
      [2, "command", "String", [], "A reference to a previously issued Command."],
      [3, "device", "Device", [], "The properties of a hardware device."],
      [7, "domain_name", "Domain-Name", [], "A network domain name."],
      [8, "email_addr", "Email-Addr", [], "A single email address."],
      [9, "features", "Features", [], "A set of items used with the query Action to determine an Actuator's capabilities."],
      [10, "file", "File", [], "Properties of a file."],
      [11, "idn_domain_name", "IDN-Domain-Name", [], "An internationalized domain name."],
      [12, "idn_email_addr", "IDN-Email-Addr", [], "A single internationalized email address."],
      [13, "ipv4_net", "IPv4-Net", [], "An IPv4 address range including CIDR prefix length."],
      [14, "ipv6_net", "IPv6-Net", [], "An IPv6 address range including prefix length."],
      [15, "ipv4_connection", "IPv4-Connection", [], "A 5-tuple of source and destination IPv4 address ranges, source and destination ports, and protocol"],
      [16, "ipv6_connection", "IPv6-Connection", [], "A 5-tuple of source and destination IPv6 address ranges, source and destination ports, and protocol"],
      [20, "iri", "IRI", [], "An internationalized resource identifier (IRI)."],
      [17, "mac_addr", "MAC-Addr", [], "A Media Access Control (MAC) address - EUI-48 or EUI-64 as defined in [[EUI]](#eui)"],
      [18, "process", "Process", [], "Common properties of an instance of a computer program as executed on an operating system."],
      [25, "properties", "Properties", [], "Data attribute associated with an Actuator"],
      [19, "uri", "URI", [], "A uniform resource identifier (URI)."]
    ]],
    ["Args", "Map", ["{1"], "", [
      [1, "start_time", "Date-Time", ["[0"], "The specific date/time to initiate the Command"],
      [2, "stop_time", "Date-Time", ["[0"], "The specific date/time to terminate the Command"],
      [3, "duration", "Duration", ["[0"], "The length of time for an Command to be in effect"],
      [4, "response_requested", "Response-Type", ["[0"], "The type of Response required for the Command: `none`, `ack`, `status`, `complete`."]
    ]],
    ["Actuator", "Choice", [], "", [
      [1, "placeholder", "String", [], "Placeholder"]
    ]],
    ["Results", "Map", ["{1"], "", [
      [1, "versions", "ArrayOf", ["*Version", "q", "[0"], "List of OpenC2 language versions supported by this Actuator"],
      [2, "profiles", "ArrayOf", ["*Nsid", "[0"], "List of profiles supported by this Actuator"],
      [3, "pairs", "Action-Targets", ["[0"], "List of targets applicable to each supported Action"],
      [4, "rate_limit", "Number", ["[0"], "Maximum number of requests per minute supported by design or policy"]
    ]],
    ["Action-Targets", "MapOf", ["*Targets", "+Action", "{1"], "Map of each action supported by this actuator to the list of targets applicable to that action"],
    ["Targets", "ArrayOf", ["*>Target", "{1", "}1", "q"], "List of JSON Pointers to Target types"],
    ["Status-Code", "Enumerated", ["="], "", [
      [102, "Processing", "an interim Response used to inform the Producer that the Consumer has accepted the Command but has not yet completed it."],
      [200, "OK", "the Command has succeeded."],
      [400, "BadRequest", "the Consumer cannot process the Command due to something that is perceived to be a Producer error (e.g., malformed Command syntax)."],
      [401, "Unauthorized", "the Command Message lacks valid authentication credentials for the target resource or authorization has been refused for the submitted credentials."],
      [403, "Forbidden", "the Consumer understood the Command but refuses to authorize it."],
      [404, "NotFound", "the Consumer has not found anything matching the Command."],
      [500, "InternalError", "the Consumer encountered an unexpected condition that prevented it from performing the Command."],
      [501, "NotImplemented", "the Consumer does not support the functionality required to perform the Command."],
      [503, "ServiceUnavailable", "the Consumer is currently unable to perform the Command due to a temporary overloading or maintenance of the Consumer."]
    ]],
    ["Artifact", "Record", ["{1"], "", [
      [1, "mime_type", "String", ["[0"], "Permitted values specified in the IANA Media Types registry, [[RFC6838]](#rfc6838)"],
      [2, "payload", "Payload", ["[0"], "Choice of literal content or URL"],
      [3, "hashes", "Hashes", ["[0"], "Hashes of the payload content"]
    ]],
    ["Device", "Map", ["{1"], "", [
      [1, "hostname", "Hostname", ["[0"], "A hostname that can be used to connect to this device over a network"],
      [2, "idn_hostname", "IDN-Hostname", ["[0"], "An internationalized hostname that can be used to connect to this device over a network"],
      [3, "device_id", "String", ["[0"], "An identifier that refers to this device within an inventory or management system"]
    ]],
    ["Domain-Name", "String", ["/hostname"], "[[RFC1034]](#rfc1034), Section 3.5"],
    ["Email-Addr", "String", ["/email"], "Email address, [[RFC5322]](#rfc5322), Section 3.4.1"],
    ["Features", "ArrayOf", ["*Feature", "{0", "}10", "q"], "An array of zero to ten names used to query an Actuator for its supported capabilities."],
    ["File", "Map", ["{1"], "", [
      [1, "name", "String", ["[0"], "The name of the file as defined in the file system"],
      [2, "path", "String", ["[0"], "The absolute path to the location of the file in the file system"],
      [3, "hashes", "Hashes", ["[0"], "One or more cryptographic hash codes of the file contents"]
    ]],
    ["IDN-Domain-Name", "String", ["/idn-hostname"], "Internationalized Domain Name, [[RFC5890]](#rfc5890), Section 2.3.2.3."],
    ["IDN-Email-Addr", "String", ["/idn-email"], "Internationalized email address, [[RFC6531]](#rfc6531)"],
    ["IPv4-Net", "Array", ["/ipv4-net"], "", [
      [1, "ipv4_addr", "IPv4-Addr", [], "IPv4 address as defined in [[RFC0791]](#rfc0791)"],
      [2, "prefix_length", "Integer", ["[0"], "CIDR prefix-length. If omitted, refers to a single host address."]
    ]],
    ["IPv4-Connection", "Record", ["{1"], "5-tuple that specifies a tcp/ip connection", [
      [1, "src_addr", "IPv4-Net", ["[0"], "IPv4 source address range"],
      [2, "src_port", "Port", ["[0"], "source service per [[RFC6335]](#rfc6335)"],
      [3, "dst_addr", "IPv4-Net", ["[0"], "IPv4 destination address range"],
      [4, "dst_port", "Port", ["[0"], "destination service per [[RFC6335]](#rfc6335)"],
      [5, "protocol", "L4-Protocol", ["[0"], "layer 4 protocol (e.g., TCP) - see [Section 3.4.2.10](#34210-l4-protocol)"]
    ]],
    ["IPv6-Net", "Array", ["/ipv6-net"], "", [
      [1, "ipv6_addr", "IPv6-Addr", [], "IPv6 address as defined in [[RFC8200]](#rfc8200)"],
      [2, "prefix_length", "Integer", ["[0"], "prefix length. If omitted, refers to a single host address."]
    ]],
    ["IPv6-Connection", "Record", ["{1"], "5-tuple that specifies a tcp/ip connection", [
      [1, "src_addr", "IPv6-Net", ["[0"], "IPv6 source address range"],
      [2, "src_port", "Port", ["[0"], "source service per [[RFC6335]](#rfc6335)"],
      [3, "dst_addr", "IPv6-Net", ["[0"], "IPv6 destination address range"],
      [4, "dst_port", "Port", ["[0"], "destination service per [[RFC6335]](#rfc6335)"],
      [5, "protocol", "L4-Protocol", ["[0"], "layer 4 protocol (e.g., TCP) - [Section 3.4.2.10](#34210-l4-protocol)"]
    ]],
    ["IRI", "String", ["/iri"], "Internationalized Resource Identifier, [[RFC3987]](#rfc3987)."],
    ["MAC-Addr", "Binary", ["/eui"], "Media Access Control / Extended Unique Identifier address - EUI-48 or EUI-64 as defined in [[EUI]](#eui)."],
    ["Process", "Map", ["{1"], "", [
      [1, "pid", "Integer", ["w0", "[0"], "Process ID of the process"],
      [2, "name", "String", ["[0"], "Name of the process"],
      [3, "cwd", "String", ["[0"], "Current working directory of the process"],
      [4, "executable", "File", ["[0"], "Executable that was executed to start the process"],
      [5, "parent", "Process", ["[0"], "Process that spawned this one"],
      [6, "command_line", "String", ["[0"], "The full command line invocation used to start this process, including all arguments"]
    ]],
    ["Properties", "ArrayOf", ["*String", "{1", "q"], "A list of names that uniquely identify properties of an Actuator."],
    ["URI", "String", ["/uri"], "Uniform Resource Identifier, [[RFC3986]](#rfc3986)."],
    ["Date-Time", "Integer", ["w0"], "Date and Time"],
    ["Duration", "Integer", ["w0"], "A length of time"],
    ["Feature", "Enumerated", [], "Specifies the results to be returned from a query features Command", [
      [1, "versions", "List of OpenC2 Language versions supported by this Actuator"],
      [2, "profiles", "List of profiles supported by this Actuator"],
      [3, "pairs", "List of supported Actions and applicable Targets"],
      [4, "rate_limit", "Maximum number of Commands per minute supported by design or policy"]
    ]],
    ["Hashes", "Map", ["{1"], "Cryptographic Hash values", [
      [1, "md5", "Binary", ["/x", "[0"], "MD5 hash as defined in [[RFC1321]](#rfc1321)"],
      [2, "sha1", "Binary", ["/x", "[0"], "SHA1 hash as defined in [[RFC6234]](#rfc6234)"],
      [3, "sha256", "Binary", ["/x", "[0"], "SHA256 hash as defined in [[RFC6234]](#rfc6234)"]
    ]],
    ["Hostname", "String", ["/hostname"], "Internet host name as specified in [[RFC1123]](#rfc1123)"],
    ["IDN-Hostname", "String", ["/idn-hostname"], "Internationalized Internet host name as specified in [[RFC5890]](#rfc5890), Section 2.3.2.3."],
    ["IPv4-Addr", "Binary", ["/ipv4-addr"], "32 bit IPv4 address as defined in [[RFC0791]](#rfc0791)"],
    ["IPv6-Addr", "Binary", ["/ipv6-addr"], "128 bit IPv6 address as defined in [[RFC8200]](#rfc8200)"],
    ["L4-Protocol", "Enumerated", [], "Value of the protocol (IPv4) or next header (IPv6) field in an IP packet. Any IANA value, [RFC5237]", [
      [1, "icmp", "Internet Control Message Protocol - [[RFC0792]](#rfc0792)"],
      [6, "tcp", "Transmission Control Protocol - [[RFC0793]](#rfc0793)"],
      [17, "udp", "User Datagram Protocol - [[RFC0768]](#rfc0768)"],
      [132, "sctp", "Stream Control Transmission Protocol - [[RFC4960]](#rfc4960)"]
    ]],
    ["Nsid", "String", ["{1", "}16"], "A short identifier that refers to a namespace."],
    ["Payload", "Choice", [], "", [
      [1, "bin", "Binary", [], "Specifies the data contained in the artifact"],
      [2, "url", "URI", [], "MUST be a valid URL that resolves to the un-encoded content"]
    ]],
    ["Port", "Integer", ["w0", "x65535"], "Transport Protocol Port Number, [[RFC6335]](#rfc6335)"],
    ["Response-Type", "Enumerated", [], "", [
      [0, "none", "No response"],
      [1, "ack", "Respond when Command received"],
      [2, "status", "Respond with progress toward Command completion"],
      [3, "complete", "Respond when all aspects of Command completed"]
    ]],
    ["Version", "String", [], "Major.Minor version number"]
  ]
}

  j_meta_schema = {
    "meta": {
      "package": "https://www.test.com",
      "roots": ["Decimal-Integer", "Binary-Fmt", "Integer-Fmts", "String-Fmts"]
    },
    "types": [
      ["Decimal-Integer", "Record", [], "", [
          [1, "u64", "Integer", ["/u64"], ""],
          [2, "i64", "Integer", ["/i64"], ""],
          [3, "non_negative_integer", "Integer", ["/nonNegativeInteger"], ""],
          [4, "negative_integer", "Integer", ["/negativeInteger"], ""],
          [5, "non_positive_integer", "Integer", ["/nonPositiveInteger"], ""],
          [6, "positive_integer", "Integer", ["/positiveInteger"], ""],
          [7, "unsigned_short", "Integer", ["/u16"], ""]
        ]],
      ["Binary-Fmt", "Record", [], "", [
          [1, "lower_x", "Binary", ["/x", "[0"], ""],
          [2, "upper_x", "Binary", ["/X", "[0"], ""],
          [3, "base64", "Binary", ["/b64", "[0"], ""]
        ]],
      ["Integer-Fmts", "Record", [], "", [
          [1, "int_date_time", "Integer", ["/date-time"], ""],
          [2, "string_date_time", "String", ["/date-time"], ""],
          [3, "int_date", "Integer", ["/date"], ""],
          [4, "string_date", "String", ["/date"], ""],
          [5, "time", "Integer", ["/time"], ""],
          [6, "string_time", "String", ["/time"], ""],
          [7, "g_year_month", "Integer", ["/gYearMonth"], ""],
          [8, "g_year", "Integer", ["/gYear"], ""],
          [9, "g_month_day", "Integer", ["/gMonthDay"], ""],
          [10, "duration_test", "Integer", ["/duration"], ""],
          [11, "day_time_duration", "Integer", ["/dayTimeDuration"], ""],
          [12, "year_month_duration", "Integer", ["/yearMonthDuration"], ""]
        ]],
      ["String-Fmts", "Record", [], "", [
          [1, "normalized_string", "String", ["/normalizedString"], ""],
          [2, "token", "String", ["/token"], ""],
          [3, "language", "String", ["/language"], ""],
          [4, "name", "String", ["/name"], ""],
          [5, "any_uri", "String", ["/anyUri"], ""],
          [6, "qname", "String", ["/QName"], ""]
        ]]
    ]
  }

  passed = False  
  try :
      j_validation = DataValidation(j_meta_schema, "OpenC2-Command", data)
      j_validation.validate()
      passed = True
  except Exception as e:
      print(e)