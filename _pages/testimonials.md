---
layout: archive
title: "Testimonials"
permalink: /testimonials/
author_profile: true
---

{% include base_path %}


<div class="grid__wrapper">
  {% for post in site.testimonials %}
    {% include archive-single.html type="grid" %}
  {% endfor %}
</div>
