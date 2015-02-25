# -*- coding: utf-8 -*-
{
    'name': 'Website Documentation',
    'category': 'Website',
    'summary': 'Website, Documentation',
    'version': '1.0',
    'description': """
Documentation Using Website, pages and google docs
To create a page you can type: http://localhost:9069/page/asda

# TODO agregar un tipo de contenido que la incruste directamente, que pegue todo este html
Se puede crear una pagina de este tipo:
<t t-name="website.ayuda2">
  <t t-call="website.layout">
    <div id="wrap" class="oe_structure oe_empty">
      <section class="mt16 mb16">
        <div class="container">
          <div class="row">
            <iframe id="google-doc-iframe" srcdoc="" style="height: 1050px; margin: 0 auto;" align="middle" frameborder="0" width="100%" height="100%" scrolling="no">
            </iframe>
         
            <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
            <script>
            $(function() {
                $.get("https://docs.google.com/document/d/1veiMNSox9Isg5gbJwbYNczW57XcosSNK_0yCvyobwxk/pub?embedded=true", function(html) {
                    $("#google-doc-iframe").attr("srcdoc", html);
                    setTimeout(function() {
                        $("#google-doc-iframe").contents().find('a[href^="http://"]').attr("target", "_blank");
                        $("#google-doc-iframe").contents().find('a[href^="https://"]').attr("target", "_blank");
                    }, 1000);
                });
            });
            </script>            
          </div>
        </div>
      </section>
    </div>
  </t>
</t>

        """,
    'author': 'ADHOC SA',
    'depends': [
        'website_forum'
    ],
    'data': [
        'data/doc_data.xml',
        'security/ir.model.access.csv',
        'views/doc.xml',
        'views/website_doc.xml',
    ],
    'demo': [
        'data/doc_demo.xml',
    ],
    'installable': True,
}
