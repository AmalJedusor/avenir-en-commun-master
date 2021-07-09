from random import choice

from django.shortcuts import render, redirect
import markdown

from .models import Chapter, Article


def home(request):
    return render(request, "home.html")


def toc(request):
    return render(request, "toc.html",{
        'chapters': Chapter.objects.all()
    })


def chapter(request, n, slug):
    chapter = Chapter.objects.get(number=n)
    return render(request, "chapter.html", {
        'chapter': chapter,
        'content': markdown.Markdown().convert(chapter.content),
    })


def section(request,c, n, slug):
    article = Article.objects.get(number=n)
    return render(request, "section.html", {
        'article': article,
        'content': markdown.Markdown().convert(article.content),
        'chapter': c,
    })


def random(request):
    article = choice(list(Article.objects.all()))
    return redirect(f'/section/{article.number}/{article.slug}')


def search(request):
    q = request.GET.get("termes")
    # entity (chapter ou article)
    #short_url -> url rapide vers l'article
    # highlights = rapide résumé ou y'a le passage
    if q is None:
         return render(request, "search.html", {
        'search_results': [],
        'search_terms' :'',
        'no_search' : True,
    })
    print(q)
    articles = Article.objects.filter(content__icontains=q)
    return render(request, "search.html", {
        'search_results': articles,
        'search_terms': q,
        'no_search': False,
        'suggestions': ['partage', 'écologie', 'bonheur', 'santé', 'industrie', 'économie', 'planification',
   'transition', 'indépendance', 'Europe', 'finance', 'protectionnisme', 'laïcité', 'coopération']
    })



'''
 public function searchAction($_format, Request $request)
    {
        $query  = $request->get('termes');

        if (null == $query and 'html' == $_format) {
            return $this->render('/search/search.html.twig', array(
                'search_results' => [],
                'search_terms'   => '',
                'no_search'      => true,
            ));
        }

        $finder = $this->get('fos_elastica.finder.app');

        $matchQuery = new \Elastica\Query\MultiMatch();
        $matchQuery->setFields(['title^3', 'body']);
        $matchQuery->setQuery($query);
        $matchQuery->setAnalyzer('app_custom_analyzer');

        $searchQuery = new \Elastica\Query();
        $searchQuery->setSize(200);
        $searchQuery->setQuery($matchQuery);

        $searchQuery->setHighlight(
        [
            'pre_tags' => ['<mark>'],
            'post_tags' => ['</mark>'],
            'fields' => [
                'body'  => [
                    'type' => 'plain'
                ],
                'title' => [
                    'type' => 'plain'
                ],
            ],
        ]);

        $jsonData = 'json' == $_format ? array() : null;

        try {

            $results = $this->formatSearchResults(
                $finder->findHybrid($searchQuery), $jsonData
            );
        } catch (\Exception $e) {
            $message = 
                'Le moteur de recherche est indisponible pour le moment. '
                .'Merci de réessayer ultérieurement.'
            ;

            return $this->createErrorResponse($message, 'homepage', [], [
                'query'     => $query,
                'exception' => $e,
            ]);
        }

        if ('json' == $_format) {
            return new JsonResponse(array(
                'success' => true,
                'query'   => $query,
                'count'   => count($results),
                'results' => $jsonData,
            ));
        }

        return $this->render('/search/search.html.twig', array(
            'search_results' => $results,
            'search_terms'   => $query,
        ));
    }

    private function formatSearchResults(array $data, array &$json = null)
    {
        $results = array();

        foreach ($data as $item) {
            $entity  = $item->getTransformed();
            $elastic = $item->getResult();
            list($hlTitle, $hlBody) = $this->processHighlights($elastic->getHighlights());
            $result  = array(
                'title'      => $hlTitle ?: $entity->getIndexableTitle(),
                'url'        => $this->get('app.url_builder')->autolink($entity, true),
                'short_url'  => $this->get('app.url_builder')->autolink($entity, true, 'short'),
                'score'      => $elastic->getScore(),
                'highlights' => $hlBody,
                'entity'     => $entity,
            );
            $results[] = $result;

            if (is_array($json)) {
                $payload = $this->render('/search/result.html.twig', array(
                    'result' => $result,
                ))->getContent();
                
                $entry = array_merge($result, array('html'  => $payload));
                unset($entry['entity']);
                
                $json [] = $entry;
            }
        }
        
        return $results;
    }

    private function processHighlights($highlights)
    {
        $punctuation = array(',', '?', '!', '.', '…', ':', ';', ' ');
        $format      = function ($text) use ($punctuation) {
            if (!$text) {
                return null;
            }

            $first = mb_substr($text, 0, 1);
            $last  = mb_substr($text, -1, 1);
            $text  = trim($text);

            if (in_array($first, $punctuation)) {
                $text = mb_substr($text, 1);
            }

            if (in_array($last, $punctuation)) {
                $text = mb_substr($text, 0, -1);
            }

            $text = trim($text);

            if ($first == mb_strtolower($first)) {
                $text = '…'.$text;
            }

            return $text;
        };

        $result = '';
        $title  = @$highlights['title'][0];

        $bodies = @$highlights['body'];
        
        if (!$bodies) {
            return array($title, $result);
        }

        $bodies = array_map($format, $bodies);
        $result .= sprintf('<span class="highlight">%s</span>', 
            implode('…</span> <span class="highlight">', $bodies)
        );

        return array($title, $result);
    }
'''