from flask import Flask, request, jsonify
from operator import itemgetter
import pg8000

app = Flask (__name__)
conn = pg8000.connect(database='mondial', user='postgres')


@app.route("/lakes")

def lake_info():
    cursor = conn.cursor()

    sort_key = request.args.get('sort_by', 'name')
    type_key = request.args.get('type', None)

    output = []

#if a type is specified, select lakes by type
    if type_key:
        cursor.execute("""SELECT name, cast(elevation as int), cast(area as int), type FROM lake WHERE type = %s""", [type_key])
# if a type is not specific, select all
    elif type_key is None:
        cursor.execute("""SELECT name, cast(elevation as int), cast(area as int), type FROM lake""")

# sort selection by specified key: area, elevation, or name
    if sort_key == 'area':
        for item in cursor.fetchall():
            output.append({'name': item[0], 'elevation': int(item[1] or 0), 'area':int(item[2] or 0), 'type': item[3]})

        output_by_area = sorted(output, key=lambda k: ('area' not in k, k.get('area', None)), reverse = True)

        return jsonify(output_by_area)

    elif sort_key == 'elevation':
        for item in cursor.fetchall():
            output.append({'name': item[0], 'elevation': int(item[1] or 0), 'area':int(item[2] or 0), 'type': item[3]})

        output_by_elevation = sorted(output, key=lambda k: ('elevation' not in k, k.get('elevation', None)), reverse = True)

        return jsonify(output_by_elevation)

    elif sort_key == 'name':
        for item in cursor.fetchall():
            output.append({'name': item[0], 'elevation': item[1], 'area':item[2], 'type': item[3]})

        output_by_name = sorted(output, key=itemgetter('name'))

        return jsonify(output_by_name)

# if not sort_key is specified then return list sorted by name
    else:
        for item in cursor.fetchall():
            output.append({'name': item[0], 'elevation': item[1], 'area':item[2], 'type': item[3]})

        output_by_name = sorted(output, key=itemgetter('name'))

        return jsonify(output_by_name)

app.run()
