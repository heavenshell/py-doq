"""{{ name }}.

{% for p in params -%}
:param {{ p.argument }}:
{% if p.annotation -%}
:type {{ p.argument }}: {{ p.annotation }}
{% endif -%}
{% endfor -%}
{% if return_type -%}
:rtype: {{ return_type }}
{% endif -%}
"""
