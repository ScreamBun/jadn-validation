from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data


j_schema = {
  "info": {
  "package": "http://docs.oasis-open.org/openc2/ns/ap-th/v1.0",
    "version": "v01-csd02-01",
    "title": "Threat Hunting Profile",
    "description": "Data definitions for Threat Hunting (TH) functions",
    "namespaces": {
      "ls": "http://docs.oasis-open.org/openc2/ns/lang/v1.0",
      "oca": "http://docs.oasis-open.org/openc2/ns/ext/oca",
      "sco": "http://docs.oasis-open.org/openc2/ns/ext/sco"
    },
    "exports": ["TH-Target", "TH-Args", "TH-Specifiers", "TH-Results"],
    "config": {
      "$MaxBinary": 1555,
      "$MaxString": 1555,
      "$MaxElements": 155,
      "$Sys": "$",
      "$TypeName": "^[A-Za-z][-:_A-Za-z0-9]{0,63}$",
      "$FieldName": "^[A-Za-z][-:_A-Za-z0-9]{0,63}$",
      "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
    }
  },
  "types": [
    ["Action", "Enumerated", [], "", [
      [3, "query", "Initiate a request for information."],
      [30, "investigate", "Task the recipient to aggregate and report information as it pertains to a security event or incident."]
    ]],
    ["Target", "Choice", [], "", [
      [9, "features", "ls:Features", [], ""],
      [1036, "th", "TH-Target", [], ""]
    ]],
    ["Args", "Map", [], "", [
      [1, "start_time", "ls:Date-Time", [], ""],
      [2, "stop_time", "ls:Date-Time", [], ""],
      [3, "duration", "ls:Duration", [], ""],
      [4, "response_requested", "ls:Response-Requested", [], ""],
      [1036, "th", "TH-Args", [], ""]
    ]],
    ["Actuator", "Enumerated", [], "", [
      [1036, "th", ""]
    ]],
    ["Results", "Map", [], "", [
      [1, "versions", "ls:Version", ["[0"], "List of OpenC2 language versions supported by this Actuator"],
      [2, "profiles", "ArrayOf", ["*ls:Nsid", "[0"], "List of profiles supported by this Actuator"],
      [3, "pairs", "Pairs", ["[0", "]0"], "List of targets applicable to each supported Action"],
      [4, "rate_limit", "Number", [], ""],
      [1036, "th", "TH-Results", [], ""]
    ]],
    ["Pairs", "Enumerated", [], "", [
      [3, "query: features, /huntflows, /datasources", ""],
      [30, "investigate: /hunt", ""]
    ]],
    ["TH-Target", "Choice", [], "TH targets defined in this profile.", [
      [1, "hunt", "String", [], "A procedure to find a set of entities in the monitored environment that associates with a cyberthreat."],
      [2, "huntflows", "Huntflow-Specifiers", [], "TH Huntflow specifiers."],
      [3, "datasources", "String", ["[0"], ""]
    ]],
    ["TH-Args", "Map", ["{0"], "TH command arguments defined in this profile.", [
      [1, "huntargs", "Huntargs", [], "Arguments for use in conjunction with hunt implementation."]
    ]],  
    ["Huntargs", "Record", ["{1"], "TH command arguments defined in this profile.", [
      [1, "string_args", "ArrayOf", ["*String", "[0"], "string arguments supplied as huntargs."],
      [2, "integer_args", "ArrayOf", ["*Integer", "[0"], "integer arguments supplied as huntargs."],
      [3, "typed_args", "Typed-Arguments", ["[0"], "Paired strings of named arguments."],
      [4, "native_oc2", "OC2-Data", ["[0"], "OC2 Language types supplied as huntargs."],
      [5, "stix", "sco:STIX-Cybersecurity-Observables", ["[0"], "STIX arguments supplied as huntargs."],
      [6, "stix_extensions", "oca:OCA-Extensions", ["[0"], "STIX arguments extended with OCA extensions supplied as huntargs. TODO add a custom stix for oca-asset and event"],
      [7, "timeranges", "Timeranges", ["[0"], "Timeranges used in the execution of a hunt."],
      [8, "datasources", "Datasource-Array", ["[0"], "Available data sources for hunting. These may be a host monitor, an EDR, a SIEM, a firewall, etc."]
    ]],   
      
    ["OC2-Data", "ArrayOf", ["*Language-Spec-Types"], "OC2-Data is an array of one or more types defined in the OpenC2 language spec"],
  
    ["Language-Spec-Types", "Choice", [], "for each track there's a file with the audio and a metadata record", [
      [1, "artifact", "ls:Artifact", ["[0"], "An array of bytes representing a file-like object or a link to that object."],
      [2, "device", "ls:Device", ["[0"], "The properties of a hardware device."], 
      [3, "domain_name", "ls:Domain-Name", ["[0"], "A network domain name."],
      [4, "email-address", "ls:Email-Addr", ["[0"], "A single email address"],   
      [5, "file", "ls:File", ["[0"], "Properties of a file."],
      [6, "hashes", "ls:Hashes", ["[0"], "Not used as an entity; use inside File or other attribute of another type. May be used as a query value."],
      [7, "hostname", "ls:Hostname", ["[0"], "Value must be a hostname as defined in [RFC1034], Section 3.1"],
      [8, "idn_domain_name", "ls:IDN-Domain-Name", ["[0"], "An internationalized domain name."],
      [9, "idn_email_address", "ls:IDN-Email-Addr", ["[0"], "A single internationalized email address."],
      [10, "ipv4_address", "ls:IPv4-Addr", ["[0"], "IPv4 address as defined in [RFC0791]."],
      [11, "ipv6_address", "ls:IPv6-Addr", ["[0"], "IPv6 address as defined in [RFC8200]."],
      [12, "ipv4_network", "ls:IPv4-Net", ["[0"], "IPv4 network targeted by hunt activity."],
      [13, "ipv6_network", "ls:IPv6-Net", ["[0"], "IPv6 network targeted by hunt activity."],
      [14, "ipv4_connection", "ls:IPv4-Connection", ["[0"], "A 5-tuple of source and destination IPv4 address ranges, source and destination ports, and protocol."],
      [15, "ipv6_connection", "ls:IPv6-Connection", ["[0"], "A 5-tuple of source and destination IPv6 address ranges, source and destination ports, and protocol."],
      [16, "iri", "ls:IRI", ["[0"], "An internationalized resource identifier (IRI)."],
      [17, "mac_address", "ls:MAC-Addr", ["[0"], "A Media Access Control (MAC) address - EUI-48 or EUI-64 as defined in [EUI]."],
      [18, "port", "ls:Port", ["[0"], "Transport Protocol Port Number, [RFC6335]"],
      [19, "process", "ls:Process", ["[0"], "Common properties of an instance of a computer program as executed on an operating system."],
      [20, "uri", "ls:URI", ["[0"], "A uniform resource identifier (URI)."]
    ]],

    ["TH-Specifiers", "Map", [], "TH actuator specifiers (may be empty)."],
    ["Huntflow-Specifiers", "Map", ["{0"], "TH Huntflow specifiers.", [
      [1, "path", "String", ["[0"], "Return huntflows at and below this filesystem location (absolute path)."],
      [2, "tags", "Tags", ["[0"], "Return huntflows with these keywords."],
      [3, "arg_types", "Specified-Arg-Types", ["[0"], "Return huntflows that take these argument types."],
      [4, "arg_names", "Specified-Arg-Names", ["[0"], "Return huntflows that take these argument types."],
      [5, "format_types", "Return-Type", ["[0"], "Return huntflows that produce these output types."],
      [6, "return_format", "Huntflow-Sections", ["[0"], "For each huntflow returned, include these data items."]
    ]],
    ["Specified-Arg-Types", "ArrayOf", ["*Arg-Type"], "Return huntflows that take these argument types."],
    ["Specified-Arg-Names", "ArrayOf", ["*Arg-Name"], "Return huntflows that take arguments with these names."],
    ["TH-Results", "Map", ["{1"], "TH results defined in this profile.", [
      [1, "huntflow_info", "Huntflow-Array", ["[0"], "Structured data returned by Query: Huntflows."],
      [2, "datasources", "Datasource-Array", ["[0"], "Datasource names and info returned by Query Datasources."],
      [3, "inv_returns", "Inv-Returns", ["[0"], "STIX SCO object returns."]
    ]],

    ["Huntflow-Array", "ArrayOf", ["*Huntflow-Info"], "Structured data returned by Query: Huntflows."],
  
    ["Inv-Returns", "ArrayOf", ["*Inv-Return", "{1"], "Array of returns from threat hunt investigations."],
  
    ["Inv-Return", "Record", [], "Data returned by a threat hunt, in various formatted types.", [
    [1, "string_returns", "ArrayOf", ["*String", "[0"], "String return from an investigation"],
    [2, "stix_sco", "sco:STIX-Cybersecurity-Observables", ["[0"], "STIX SCO object returns"]
    ]],

    ["Timeranges", "ArrayOf", ["*Timerange"], "timeranges used in the execution of a hunt."],
    ["Timerange", "Choice", [], "a timerange used in the execution of a hunt.", [
      [1, "timerange_absolute", "Timerange-Abs", ["[0"], "Absolute timerange, defined by a start and end time in ISO 8601 format."],
      [2, "timerange_relative", "Timerange-Rel", ["[0"], "Relative timerange, example '3, Days' for last 3 days."]
    ]],
    ["Time-Unit", "Enumerated", [], "Time Unit Keywords.", [
      [1, "Days", ""],
      [2, "Hours", ""], 
      [3, "Minutes", ""], 
      [4, "Seconds", ""]
    ]],
    ["Timerange-Abs", "Record", ["{2"], "Absolute timerange, defined by a start and end time in ISO 8601 format.", [
      [1, "hunt_start_time", "timestamp", [], "Start time, as a STIX time string."],
      [2, "hunt_stop_time", "timestamp", [], "Stop time, as a STIX time string."]
    ]],
    ["Timerange-Rel", "Record", ["{2"], "Relative timerange, example '3, Days' for last 3 days.", [
      [1, "number", "Integer", ["[1"], "Number of specified Time Units used in Relative Timerange."],
      [2, "time_unit", "Time-Unit", ["[1"], "Time Unit Keywords."]
    ]],
    ["Return-Type", "Record", ["{2"], "Variable names and types expected as returns when using a Huntflow.", [
      [1, "var_name", "Arg-Name", ["[1"], "Variable name to be returned by use of Huntflow."],
      [2, "var_type", "Arg-Type", ["[1"], "Type of data to be returned by use of Huntflow."]
    ]],
    ["Datasource", "Record", ["{1"], "Datasource names and tags required for use with a particular Huntflow.", [
      [1, "ds_name", "String", ["[1"], "Name of a Datasource used by a Huntflow in Kestrel runtime."],
      [2, "ds_tags", "Tags", ["[0"], "Tags applied to a Datasource for search or filter purposes."]
    ]],
    ["Huntflow-Sections", "ArrayOf", ["*Huntflow-Section", "{0"], "For each huntflow returned, include these data items."],
    ["Huntflow-Section", "Enumerated", [], "Data format to be returned by Query Huntflows. If none specified, return all.", [
      [1, "path", "Specifies the return should include the path to each Huntflow specified by the query conditions."],
      [2, "uniqueId", "Specifies the return should include the ID of each Huntflow specified by the query conditions."], 
      [3, "version", "Specifies the return should include the ID of each Huntflow specified by the query conditions."], 
      [4, "args_required", "Specifies the returned data should include the required arguments for the available Huntflows."],
      [5, "expected_returns", "Specifies the returned data should include the expected returns for the available Huntflows."],
      [6, "script", "Specifies the returned data should include the full text of the Huntflow for each available Huntflow."]
    ]],
    ["Huntflow-Info", "Record", ["{1"], "Structured data returned by Query: Huntflows with specifiers for specific info.", [
      [1, "path", "String", ["[0"], "Path used to identify a Huntflow in place of a name."],
      [2, "uniqueId", "Integer", ["[0"], "Unique ID associated with a specified Huntflow."], 
      [3, "version", "String", ["[0"], "Unique ID associated with a specified Huntflow."], 
      [4, "args_required", "Typed-Arguments", ["[0"], "List of arguments used in the specified Huntflow."],
      [5, "expected_returns", "Typed-Arguments", ["[0"], "Data returned by the specified Huntflows."],
      [6, "script", "String", ["[0"], "Text of Hunt logic implemented by specified Huntflow."]
    ]],
    ["Datasource-Array", "ArrayOf", ["*Datasource"], "An Array of Datasources, with multiple uses in Threathunting"],
    ["Tags", "ArrayOf", ["*String"], "Tags applied for search or filter purposes."],   

    ["Typed-Arguments", "MapOf", ["+Arg-Name", "*Typed-Values"], "Argument names and types tied to a specific Huntflow."],
    ["Arg-Name", "String", [], "Argument names used by a Huntflow. Follow C variable naming conventions. Examples include name, src_port, and x_unique_id."],
    ["Typed-Values", "MapOf", ["+Arg-Type", "*Arg-Values"], "Argument types and values used to investivate a specific Huntflow."],
    ["Arg-Type", "String", [], "Argument types used by a Huntflow. Follow STIX naming conventions, with lowercase characters and hyphens replacing spaces. Common types include process, file, and network-traffic."],
    ["Arg-Values", "ArrayOf", ["*Arg-Value"], "Argument values used by a Huntflow."],
    ["Arg-Value", "String", [], "Argument value used by a Huntflow."],

    ["timestamp", "String", ["%^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"], ""]

  ]
}

def test_th_target():
    root = "TH-Target"
    
    valid_test_1 = {
            "hunt": "./hunts/huntflow/query_net_traffic_stixdata.hf"
    }
    
    valid_test_2 = {
            "huntflows": {
            "path": "/hunts/",
            "tags": ["test 1", "test 2"],
            "arg_types": ["network-traffic1", "network-traffic2"],
            "arg_names": ["x_unique_id.", "x_unique_id.2"],
            "format_types": {
                "var_name": "test",
                "var_type": "test"
            },
            "return_format": ["version"]
            }
    }
    
    valid_test_3 = {
        "datasources": "test"
    }
    
    valid_data_list = [
        valid_test_1,
        valid_test_2,
        valid_test_3
    ] 
    
    
    invalid_test_1 = {
            "hunt": True
    }
    
    invalid_test_2 = {
            "huntflows": {
                "path": "/hunts/",
                "tagz": ["test 1", "test 2"],
                "arg_types": ["network-traffic1", "network-traffic2"],
                "arg_names": ["x_unique_id.", "x_unique_id.2"],
                "format_types": {
                    "var_name": "test",
                    "var_type": "test"
                },
                "return_format": ["version"]
            }
    }
    
    invalid_test_3 = {
        "datasources": 111
    }    
    
    invalid_data_list = [
        invalid_test_1,
        invalid_test_2,
        # invalid_test_3
    ]
    
    # err_count = validate_valid_data(j_schema, root, valid_data_list)
    # assert err_count == 0
    
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)